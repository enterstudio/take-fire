import argparse
from itertools import product
import json
import os
from subprocess import run


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('task_file', type=load_json)
    args = parser.parse_args()

    run('globus login', shell=True)
    destination = get_globus_path(args.task_file['destination'])
    dst_ep_id = args.task_file['destination']['endpoint']['id']
    run(f'globus endpoint is-activated {dst_ep_id}', shell=True)
    sims = load_json('sims.json')
    for task in args.task_file['tasks']:
        source = get_globus_path(sims[task['series']])
        src_ep_id = sims[task['series']]['endpoint']['id']
        run(f'globus endpoint is-activated {src_ep_id}', shell=True)
        label = task['name']
        transfer_file = generate_batch_transfer_file(task, sims)
        print(f'globus transfer {source} {destination}'
              f' --batch --label {label} < {transfer_file}')
        run(f'globus transfer {source} {destination}'
            f' --batch --label {label} < {transfer_file}', shell=True)


def load_json(path):
    return json.load(open(path))


def get_globus_path(info):
    return ':'.join([info['endpoint']['id'], info['directory']])


def generate_batch_transfer_file(task, sims):
    file_list = []
    series = sims[task['series']]
    for sim in task['simulations']:
        sim_dir = series['simulations'][sim]
        sim_file_list = []
        for snap_num in task['snapshots']:
            sim_file_list += expand(series['snapshot'], snap_num=snap_num)
        for halo_num in task['halos']:
            sim_file_list += expand(series['halo'], halo_num=halo_num)
        sim_file_list = [os.path.join(sim_dir, f) for f in sim_file_list]
        file_list += sim_file_list
    transfer_file = 'transfer_' + task['name'] + '.txt'
    open(transfer_file, 'w')
    with open(transfer_file, 'a') as f:
        for path in file_list:
            f.write(path + ' ' + path + '\n')
    return str(transfer_file)


def expand(formatter, **kwargs):
    if 'expand' in formatter:
        # Expand parameters
        e = formatter['expand']
        return [formatter['template'].format(**params, **kwargs) for params in
                [dict(zip(e.keys(), v)) for v in product(*e.values())]]
    else:
        return [formatter['template'].format(**kwargs)]


if __name__ == '__main__':
    main()
