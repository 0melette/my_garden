#!/usr/bin/env python3
"""Compile the public Obsidian catalogue to the consumer JSON contract."""
from __future__ import annotations
import argparse
import calendar
import math
import json
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = {'Summary':'summary','Sowing':'sowing_notes','Care':'care_notes','Management':'management_notes','Harvest':'yield_wording','Uses':'uses_notes'}
ALIASES = {'catalogue_id':'id','sun':'sun_needs','water':'water_needs','spacing_cm':'in_row_spacing_cm','feeder':'feeder_type'}
FIELDS = ('slug common_name scientific_name family created_at yield_qty row_spacing_cm succession_interval_days harvest_window_weeks soil_ph_min soil_ph_max yield_unit source_url notion_url forest_layer part_used plant_group plant_category variety_name').split()
OPTIONAL = {'plant_group','plant_category','variety_name'}
NUMBERS = {'yield_qty','spacing_cm','row_spacing_cm','succession_interval_days','harvest_window_weeks','soil_ph_min','soil_ph_max'}
RELATIONS = {'pests':('pests','plant_pests'),'diseases':('diseases','plant_diseases'),'functions':('function_tags','plant_function_tags'),'uses':('uses','plant_uses')}
REFERENCE_FOLDERS = {'rotation_groups':'Rotation groups','pests':'Pests','diseases':'Diseases','function_tags':'Functions','uses':'Uses'}
MONTHS = {calendar.month_abbr[i]:i for i in range(1,13)}


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader,node,deep=False):
    result={}
    for k,v in node.value:
        key=loader.construct_object(k,deep=deep)
        if key in result: raise ValueError(f'Duplicate YAML property: {key}')
        result[key]=loader.construct_object(v,deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,unique_mapping)


def read_note(path):
    text=path.read_text(encoding='utf-8')
    match=re.match(r'\A---\s*\n(.*?)\n---\s*\n(.*)\Z',text,re.S)
    if not match: raise ValueError(f'{path.name}: missing YAML properties')
    props=yaml.load(match[1],Loader=UniqueLoader)
    if not isinstance(props,dict):raise ValueError(f'{path.name}: properties must be a mapping')
    return props,match[2]


def sections(body):
    result={}
    for match in re.finditer(r'^## ([^\n]+)\n(.*?)(?=^## |\Z)',body,re.M|re.S):
        title=match[1].strip()
        if title in result:raise ValueError(f'Duplicate section: {title}')
        result[title]=re.sub(r'<!--.*?-->','',match[2],flags=re.S).strip() or None
    return result


def write_note(path,props,body):
    content='---\n'+yaml.safe_dump(props,sort_keys=False,allow_unicode=True,width=1000)+'---\n\n'+body.lstrip()
    temporary=path.with_suffix('.md.tmp');temporary.write_text(content,encoding='utf-8');temporary.replace(path)


def target(value):
    if not isinstance(value,str):raise ValueError(f'Expected a name/link, got {value!r}')
    if not value.startswith('[['):return value
    return value[2:].removesuffix(']]').split('|')[0].split('/')[-1].removesuffix('.md')


def as_list(props,key):
    value=props.get(key) or []
    if not isinstance(value,list):raise ValueError(f'{key} must be a list')
    if len(value)!=len({str(v) for v in value}):raise ValueError(f'Duplicate values in {key}')
    return value


def compile_catalogue(root=ROOT,assign_ids=False):
    meta,_=read_note(root/'Catalogue.md')
    tables={}; lookups={}; source_paths=[root/'Catalogue.md']
    for table,folder in REFERENCE_FOLDERS.items():
        rows=[]; lookup={}; ids=set()
        for path in sorted((root/'References'/folder).rglob('*.md')):
            props,body=read_note(path); rid=props['id']; name=props['name']
            if type(rid)!=int or rid<=0 or rid in ids or name in lookup:raise ValueError(f'{path}: invalid/duplicate reference')
            ids.add(rid);lookup[name]=rid
            row={'id':rid,'name':name}
            if table=='rotation_groups':row.update(feeder_weight=props.get('feeder_weight'),is_rotation_exempt=props.get('is_rotation_exempt',0))
            else:row['description']=sections(body).get('Description')
            rows.append(row);source_paths.append(path)
        tables[table]=sorted(rows,key=lambda r:r['id']);lookups[table]=lookup
    all_notes=[];ids=set();slugs=set();updates=[]; published=[]
    for path in sorted((root/'Plants').glob('*.md')):
        p,b=read_note(path)
        if p.get('kind')!='plant':raise ValueError(f'{path.name}: kind must be plant')
        if p.get('status') not in {'draft','published'}:raise ValueError(f'{path.name}: status must be draft or published')
        if p.get('catalogue_id') is not None:
            pid=p['catalogue_id']
            if type(pid)!=int or pid<=0 or pid in ids:raise ValueError(f'{path.name}: duplicate/invalid catalogue_id')
            ids.add(pid)
        all_notes.append((path,p,b))
    next_id=max(ids or {0})+1
    for path,p,b in all_notes:
        if p['status']=='draft':continue
        for field in ['common_name','scientific_name']:
            if not isinstance(p.get(field),str) or not p[field].strip() or '{{' in p[field]:raise ValueError(f'{path.name}: fill {field} before publishing')
        changed=False
        if p.get('catalogue_id') is None:
            if not assign_ids:raise ValueError(f'{path.name}: run export with --assign-ids to allocate a permanent ID')
            p['catalogue_id']=next_id;next_id+=1;changed=True
        if not p.get('slug'):
            if not assign_ids:raise ValueError(f'{path.name}: fill slug or run --assign-ids')
            p['slug']=re.sub(r'[^a-z0-9]+','-',p['common_name'].lower()).strip('-');changed=True
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',p['slug']) or p['slug'] in slugs:raise ValueError(f'{path.name}: duplicate/invalid slug')
        slugs.add(p['slug'])
        for field in NUMBERS:
            v=p.get(field)
            if v is not None and (type(v) not in (int,float) or not math.isfinite(v) or v<0):raise ValueError(f'{path.name}: {field} must be a non-negative number or empty')
        lo,hi=p.get('soil_ph_min'),p.get('soil_ph_max')
        if (lo is not None and lo>14) or (hi is not None and hi>14) or (lo is not None and hi is not None and lo>hi):raise ValueError(f'{path.name}: invalid soil pH range')
        if p.get('sun') not in (None,'','Not recorded','full sun','part shade','full shade'):raise ValueError(f'{path.name}: unsupported sunlight value')
        if p.get('water') not in (None,'','Not recorded','low','moderate','high'):raise ValueError(f'{path.name}: unsupported water value')
        sec=sections(b)
        if changed:updates.append((path,p,b))
        published.append((path,p,b,sec));source_paths.append(path)
    plant_lookup={path.stem:p['catalogue_id'] for path,p,_,_ in published}
    tables.update({name:[] for name in ['plant_references','planting_months','plant_images','plant_pests','plant_diseases','plant_function_tags','plant_uses','plant_companions']})
    regional=[]
    for path,p,b,sec in published:
        pid=p['catalogue_id'];row={}
        for field in FIELDS:
            if field not in OPTIONAL or field in p:row[field]=p.get(field)
        for key,field in ALIASES.items():row[field]=p.get(key) if p.get(key) not in ('','Not recorded') else None
        for title,field in SECTIONS.items():row[field]=sec.get(title)
        estimates=as_list(p,'estimated_fields');row['estimated_fields']=json.dumps(estimates) if estimates else None
        rotation=p.get('rotation_group');row['rotation_group_id']=lookups['rotation_groups'].get(target(rotation)) if rotation else None
        if rotation and row['rotation_group_id'] is None:raise ValueError(f'{path.name}: unknown rotation group {rotation}')
        tables['plant_references'].append(row)
        for month in as_list(p,'planting_months'):
            if month not in MONTHS:raise ValueError(f'{path.name}: use month abbreviations Jan to Dec')
            n=MONTHS[month];tables['planting_months'].append({'id':pid*100+n,'plant_reference_id':pid,'month_number':n})
        photo=p.get('photo')
        if photo:
            photo_path=photo.removeprefix('[[').removesuffix(']]')
            expected='localdata/plant_images/'
            if not photo_path.startswith(expected) or '/' in photo_path[len(expected):] or not (root/photo_path).is_file():raise ValueError(f'{path.name}: photo must link to a file in {expected}')
            tables['plant_images'].append({'id':pid,'plant_reference_id':pid,'filename':Path(photo_path).name})
            manifest=json.loads((root/'localdata/plant-image-sources.json').read_text())
            if not any(m['filename']==Path(photo_path).name for m in manifest['images']):raise ValueError(f'{path.name}: add photo attribution to plant-image-sources.json')
        for key,(ref_table,link_table) in RELATIONS.items():
            for item in as_list(p,key):
                name=target(item)
                if name not in lookups[ref_table]:raise ValueError(f'{path.name}: unknown {key}: {name}')
                tables[link_table].append({'plant_id':pid,'tag_id':lookups[ref_table][name]})
        seen_companions=set()
        for relation in as_list(p,'companions'):
            if not isinstance(relation,dict):raise ValueError(f'{path.name}: companions must contain plant/function/notes mappings')
            other=plant_lookup.get(target(relation['plant']));function=lookups['function_tags'].get(target(relation['function']))
            if other is None or function is None or other==pid:raise ValueError(f'{path.name}: companion must be another published plant with a known function')
            key=(other,function)
            if key in seen_companions:raise ValueError(f'{path.name}: duplicate companion')
            seen_companions.add(key)
            tables['plant_companions'].append({'plant_id':pid,'companion_id':other,'function_id':function,'notes':relation.get('notes')})
        if p.get('calendar_region')=='Sydney / warm temperate':regional.append(pid)
    for name,rows in tables.items():rows.sort(key=lambda r:tuple(str(r.get(k,'')) for k in sorted(r)))
    tables['plant_references'].sort(key=lambda r:r['id'])
    payload={'snapshot_format':1,'exported_at':str(meta['catalogue_updated'])+'T00:00:00+00:00','schema_version':meta['schema_version'],'tables':tables,
             'regional_guidance':{'region':'Sydney / warm temperate','plant_ids':sorted(regional),'details':'Plant Markdown sowing notes are authoritative. Earlier records retain their original calendar context.'}}
    # Complete validation happens before any source note is changed.
    for path,p,b in updates:write_note(path,p,b)
    return payload


def export(root,output,check=False,assign_ids=False):
    payload=compile_catalogue(root,assign_ids)
    content=json.dumps(payload,indent=2,ensure_ascii=False)+'\n'
    if check:
        if not output.is_file() or output.read_text()!=content:raise ValueError('Generated JSON is stale. Run python scripts/export_catalogue.py.')
    else:
        output.parent.mkdir(parents=True,exist_ok=True);tmp=output.with_suffix('.json.tmp');tmp.write_text(content,encoding='utf-8');tmp.replace(output)
    return payload


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=ROOT)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--assign-ids',action='store_true')
    args=parser.parse_args()
    if args.check and args.assign_ids:parser.error('--check cannot mutate source IDs')
    try:payload=export(args.root,args.output or args.root/'snapshots/almanac-catalogue.json',args.check,args.assign_ids)
    except (ValueError,KeyError,yaml.YAMLError) as e:sys.exit(f'Catalogue validation failed: {e}')
    print(f'{"Checked" if args.check else "Exported"} {len(payload["tables"]["plant_references"])} published plants from Markdown.')

if __name__=='__main__':main()
