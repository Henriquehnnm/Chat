# main.py
#
# Copyright 2025 Vegeta
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import gi
import os
import webbrowser
import socket
from gi.repository import Gtk, Gio, Adw, WebKit, GLib

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('WebKit', '6.0')

class ChatWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(1200, 800)
        self.set_title("Chat")

        # Diretório para persistência dos dados do navegador
        data_dir = os.path.expanduser("~/.local/share/chat")
        os.makedirs(data_dir, exist_ok=True)

        # Widget principal
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(self.box)

        # Cabeçalho com botões de navegação
        self.header = Adw.HeaderBar()
        self.box.append(self.header)

        # Botão voltar
        self.btn_voltar = Gtk.Button(icon_name="go-previous-symbolic")
        self.btn_voltar.connect("clicked", self.voltar)
        self.header.pack_start(self.btn_voltar)

        # Botão avançar
        self.btn_avancar = Gtk.Button(icon_name="go-next-symbolic")
        self.btn_avancar.connect("clicked", self.avancar)
        self.header.pack_start(self.btn_avancar)

        # Botão de recarregar
        self.btn_recarregar = Gtk.Button(icon_name="view-refresh-symbolic")
        self.btn_recarregar.connect("clicked", self.recarregar)
        self.header.pack_start(self.btn_recarregar)

        # Menu hambúrguer seguindo GNOME HIG
        self.menu_button = Gtk.MenuButton(icon_name="open-menu-symbolic")
        self.header.pack_end(self.menu_button)

        # Criação do menu usando Gtk.Builder (seguindo GNOME HIG)
        self.create_menu()

        # Criação do WebView com configurações personalizadas (padrão)
        self.webview = WebKit.WebView()

        # Configurações do WebView
        settings = WebKit.Settings()
        settings.set_enable_javascript(True)
        settings.set_enable_developer_extras(True)
        settings.set_enable_media_stream(True)  # Para funcionalidades de áudio
        settings.set_enable_mediasource(True)
        settings.set_allow_modal_dialogs(True)
        settings.set_enable_webgl(True)
        settings.set_enable_html5_local_storage(True)
        settings.set_enable_page_cache(True)
        # Configuração do user-agent para parecer um navegador Chrome real
        settings.set_user_agent("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

        self.webview.set_settings(settings)

        # Configura os handlers de permissão
        self.webview.connect("permission-request", self.on_permission_request)
        self.webview.connect("load-changed", self.on_webview_load_changed)

        # Scroll para o WebView
        self.scrolled = Gtk.ScrolledWindow()
        self.scrolled.set_child(self.webview)
        self.scrolled.set_hexpand(True)
        self.scrolled.set_vexpand(True)
        self.box.append(self.scrolled)

        # Carrega o Chat
        self.carregar_chat()

        # Mostrar a janela
        self.present()

    def create_menu(self):
        """Cria o menu seguindo as GNOME HIG"""
        # Criação do menu usando Gtk.Builder
        builder = Gtk.Builder()
        
        # Define o XML do menu seguindo as diretrizes do GNOME
        menu_xml = """
        <interface>
          <menu id="app-menu">
            <section>
              <item>
                <attribute name="label">Sobre</attribute>
                <attribute name="action">app.about</attribute>
              </item>
            </section>
            <section>
              <item>
                <attribute name="label">Contribuir</attribute>
                <attribute name="action">app.contribute</attribute>
              </item>
            </section>
            <section>
              <item>
                <attribute name="label">Abrir no navegador externo</attribute>
                <attribute name="action">app.open-external</attribute>
              </item>
            </section>
          </menu>
        </interface>
        """
        
        builder.add_from_string(menu_xml)
        menu = builder.get_object("app-menu")
        
        # Configura o menu no botão
        self.menu_button.set_menu_model(menu)
        
        # Configura as ações do menu
        self.setup_menu_actions()

    def setup_menu_actions(self):
        """Configura as ações do menu"""
        # Ação para "Sobre"
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.on_about)
        self.get_application().add_action(about_action)
        
        # Ação para "Contribuir"
        contribute_action = Gio.SimpleAction.new("contribute", None)
        contribute_action.connect("activate", self.on_contribute)
        self.get_application().add_action(contribute_action)
        
        # Ação para "Abrir no navegador externo"
        external_action = Gio.SimpleAction.new("open-external", None)
        external_action.connect("activate", self.on_open_external)
        self.get_application().add_action(external_action)

    def verificar_conexao(self):
        """Verifica se há conexão com a internet (tentando acessar duckduckgo.com)"""
        try:
            socket.create_connection(("duckduckgo.com", 80), timeout=2)
            return True
        except OSError:
            return False

    def mostrar_erro_conexao(self):
        """Mostra uma tela amigável de erro de conexão"""
        # Remove o WebView se já estiver na tela
        if self.scrolled in self.box:
            self.box.remove(self.scrolled)
        # Cria tela de erro
        self.tela_erro = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        self.tela_erro.set_vexpand(True)
        self.tela_erro.set_hexpand(True)
        self.tela_erro.set_halign(Gtk.Align.CENTER)
        self.tela_erro.set_valign(Gtk.Align.CENTER)
        # Ícone
        icone = Gtk.Image.new_from_icon_name("network-error-symbolic")
        icone.set_pixel_size(96)
        self.tela_erro.append(icone)
        # Mensagem
        label = Gtk.Label(label="Sem conexão com a internet!\nVerifique sua conexão e tente novamente.")
        label.set_justify(Gtk.Justification.CENTER)
        self.tela_erro.append(label)
        # Botão tentar novamente
        btn_tentar = Gtk.Button(label="Tentar novamente")
        btn_tentar.connect("clicked", self.tentar_novamente)
        self.tela_erro.append(btn_tentar)
        self.box.append(self.tela_erro)

    def tentar_novamente(self, widget):
        if self.verificar_conexao():
            self.box.remove(self.tela_erro)
            self.box.append(self.scrolled)
            self.carregar_chat()
        else:
            # Pisca a tela de erro
            self.tela_erro.set_opacity(0.5)
            Gtk.Widget.queue_draw(self.tela_erro)
            GLib.timeout_add(200, lambda: self.tela_erro.set_opacity(1))

    def carregar_chat(self):
        """Carrega o chat de IA do DuckDuckGo, mas só se houver internet"""
        if not self.verificar_conexao():
            self.mostrar_erro_conexao()
            return
        self.webview.load_uri("https://duckduckgo.com/chat")
        self.set_title("Chat")
        self.atualizar_botoes_navegacao()

    def on_webview_load_changed(self, webview, load_event):
        """Atualiza a interface quando a página é carregada"""
        if load_event == WebKit.LoadEvent.FINISHED:
            self.atualizar_botoes_navegacao()

    def on_permission_request(self, webview, request):
        """Lida com solicitações de permissão (microfone, câmera, etc)"""
        request.allow()
        return True

    def voltar(self, widget):
        if self.webview.can_go_back():
            self.webview.go_back()

    def avancar(self, widget):
        if self.webview.can_go_forward():
            self.webview.go_forward()

    def recarregar(self, widget):
        self.webview.reload()

    def atualizar_botoes_navegacao(self):
        """Atualiza o estado dos botões de navegação"""
        self.btn_voltar.set_sensitive(self.webview.can_go_back())
        self.btn_avancar.set_sensitive(self.webview.can_go_forward())

    def on_about(self, action, param):
        about = Adw.AboutWindow(
            transient_for=self,
            application_name="Chat",
            version="1.0",
            comments="Navegador simples para IA do DuckDuckGo. Feito seguindo as GNOME HIG.",
            website="https://duckduckgo.com/chat",
            developers=["Henrique Sardinha"],
            license_type=Gtk.License.GPL_3_0,
            issue_url="https://github.com/Henriquehnnm/",
            application_icon="org.vegeta.Chat",
        )
        about.present()

    def on_contribute(self, action, param):
        """Abre a janela de contribuição seguindo GNOME HIG"""
        # Cria o diálogo de contribuição usando Adw.MessageDialog
        dialog = Adw.MessageDialog(
            transient_for=self,
            heading="Contribuir para o Chat",
            body="Ajude a melhorar o Chat! Suas contribuições são muito bem-vindas.",
            close_response="close"
        )
        
        # Adiciona botão para abrir o guia de contribuição
        dialog.add_response("guide", "Ver guia de contribuição")
        dialog.add_response("close", "Fechar")
        
        # Configura as ações dos botões
        dialog.connect("response", self.on_contribute_response)
        
        dialog.present()

    def on_contribute_response(self, dialog, response):
        """Lida com as respostas do diálogo de contribuição"""
        if response == "guide":
            webbrowser.open("https://github.com/Henriquehnnm/Chat/blob/main/Contribute.md")
        dialog.close()

    def on_open_external(self, action, param):
        webbrowser.open("https://duckduckgo.com/chat")

class ChatApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='org.vegeta.Chat',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS
                         resource_base_path='/org/vegeta/Chat')
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        self.win = ChatWindow(application=app)

    def on_about_action(self, *args):
        """Callback for the app.about action."""
        about = Adw.AboutDialog(application_name='chat',
                                application_icon='org.vegeta.Chat',
                                developer_name='Vegeta',
                                version='0.1.0',
                                developers=['Vegeta'],
                                copyright='© 2025 Vegeta')
        # Translators: Replace "translator-credits" with your name/username, and optionally an email or URL.
        about.set_translator_credits(_('translator-credits'))
        about.present(self.props.active_window)

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print('app.preferences action activated')

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = ChatApplication()
    return app.run(sys.argv)

if __name__ == '__main__':
    main("1.0")
