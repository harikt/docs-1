#!/usr/bin/env python3

from os import listdir
from os.path import realpath, isfile, join, dirname, basename
from shutil import copyfile
from sys import argv
from markdown import markdown

root_path = dirname(__file__)
build_path = join(root_path, 'build')
content_files = [
	'index.md',
	'installation.md',
	'configuration.md',
	'routing.md',
	'dependency-injection.md',
	'templating.md',
	'error-handling.md',
	'database.md',
	'console.md',
	'extension.md',
]

if len(argv) > 1:
	base_href = argv[1]
else:
	base_href = 'http://localhost'
if not base_href.endswith('/'):
	base_href += '/'

print('root_path:', root_path)
print('build_path:', build_path)
print('base_href:', base_href)


def get_content_files():
	src_path = join(root_path, 'content')
	return [join(src_path, f) for f in content_files]


def generate_html_files():
	with open(join(root_path, 'templates', 'main.html')) as f:
		template = f.read()

	with open(join(root_path, 'partials', 'chapters.html')) as f:
		chapters = f.read().strip()

	with open(join(root_path, 'partials', 'links.html')) as f:
		links = f.read().strip()

	concat_content = ''

	for path in get_content_files():
		print('IN: ', path)
		with open(path) as f:
			md_content = f.read()
		content = markdown(md_content)

		header_id = basename(path).split('.')[0]
		if 'index' in path:
			header_id = 'introduction'
		concat_content += content.replace('<h1>',
			'<h1 id="{}">'.format(header_id))

		title = 'Autarky Documentation'
		if 'index' not in path:
			title = md_content.split('\n')[0].replace('# ', '') + ' - ' + title

		output = template.format(
			title=title,
			content=content.strip(),
			chapters=chapters,
			links=links,
			base_href=base_href
		)
		out_path = join(build_path, basename(path)) \
			.replace('.md', '.html')
		print('OUT:', out_path)
		with open(out_path, 'w') as f:
			f.write(output)

	chapters = chapters \
		.replace('href=""', 'href="introduction"') \
		.replace('href="', 'href="all#')

	output = template.format(
		title='Autarky Documentation',
		content=concat_content,
		chapters=chapters,
		links=links,
		base_href=base_href
	)
	out_path = join(build_path, 'all.html')
	print('OUT:', out_path)
	with open(out_path, 'w') as f:
		f.write(output)


def copy_assets():
	assets_path = join(root_path, 'assets')
	for filename in listdir(assets_path):
		path = join(assets_path, filename)
		print('IN: ', path)
		out_path = join(build_path, basename(path))
		print('OUT:', out_path)
		copyfile(path, out_path)


def main():
	generate_html_files()
	copy_assets()

if __name__ == '__main__':
	main()
