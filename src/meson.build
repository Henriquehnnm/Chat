pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'chat'
gnome = import('gnome')

gnome.compile_resources('chat',
  'chat.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

chat_sources = [
  '__init__.py',
  'main.py',
]

install_data(chat_sources, install_dir: moduledir)

# Instalar o script principal
configure_file(
  input: 'main.py',
  output: 'chat',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x'
)
