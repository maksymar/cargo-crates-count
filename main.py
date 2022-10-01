#!/usr/bin/python3
import toml
from pathlib import Path


def read(path):
    with open(path, 'r') as f:
        return f.read()


def write(path, text):
    with open(path, 'w') as f:
        return f.write(text)


def calculate_frequency(data, group, packages):
    frequency = {}
    for e in data:
        for name in e.get('cargo_toml', {}).get(group, {}):
            if name in packages:
                continue
            frequency[name] = frequency.get(name, 0) + 1
    return frequency


def main():
    source_dir = './../ic'
    output_file = './count.csv'

    # Cargo.toml files.
    data = [
        {
            'cargo_path': path,
            'cargo_toml': toml.loads(read(path)),
        }
        for path in Path(source_dir).rglob('Cargo.toml')
    ]
    data = [x for x in data if len(x.get('cargo_toml', '')) > 0]

    # IC packages.
    packages = [
        x.get('cargo_toml', {}).get('package', {}).get('name')
        for x in data
    ]
    packages = set([x for x in packages if x is not None])

    # Count frequencies.
    result = {}
    for group in ['dependencies', 'dev-dependencies', 'build-dependencies']:
        result[group] = calculate_frequency(data, group, packages)

    # Generate CSV data.
    csv = []
    for group, frequency in result.items():
        for name, count in frequency.items():
            csv.append({
                'group': group,
                'name': name,
                'count': count,
            })

    # Sort by name, ascending.
    csv = sorted(csv, key=lambda x: x['name'], reverse=False)
    # Sort by count, descending.
    csv = sorted(csv, key=lambda x: x['count'], reverse=True)
    # Sort by group, ascending.
    csv = sorted(csv, key=lambda x: x['group'], reverse=False)

    # Generate CSV table.
    table = ['group,name,count']
    for entry in csv:
        group = entry['group']
        name = entry['name']
        count = entry['count']
        table.append(f'{group},{name},{count}')

    # Write CSV to file.
    text = '\n'.join(table)
    write(output_file, text)


if __name__ == '__main__':
    main()
