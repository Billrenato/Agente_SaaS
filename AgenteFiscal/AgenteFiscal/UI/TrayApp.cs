using System;
using System.Drawing;
using System.Windows.Forms;
using AgenteFiscal.Core;
using AgenteFiscal.Utils;

namespace AgenteFiscal.UI
{
    public static class TrayApp
    {
        static NotifyIcon tray;
        static XmlMonitor monitor;

        public static void Start()
        {
            var config = ConfigManager.Load();

            monitor = new XmlMonitor();
            monitor.Start(config.XmlPath);

            tray = new NotifyIcon();

            tray.Icon = SystemIcons.Application;
            tray.Text = "Agente Fiscal";
            tray.Visible = true;

            ContextMenuStrip menu = new ContextMenuStrip();

            menu.Items.Add("Configurações", null, OpenConfig);
            menu.Items.Add("Sair", null, Exit);

            tray.ContextMenuStrip = menu;

            Logger.Log("Agente iniciado");
        }

        static void OpenConfig(object sender, EventArgs e)
        {
            ConfigForm form = new ConfigForm();
            form.Show();
        }

        static void Exit(object sender, EventArgs e)
        {
            Logger.Log("Agente finalizado");
            Environment.Exit(0);
        }
    }
}