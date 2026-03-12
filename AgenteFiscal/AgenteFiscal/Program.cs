using System;
using System.Windows.Forms;
using AgenteFiscal.Utils;
using AgenteFiscal.UI;

namespace AgenteFiscal
{
    internal static class Program
    {
        [STAThread]
        static void Main()
        {
            ApplicationConfiguration.Initialize();

            if (!ConfigManager.Exists())
            {
                Application.Run(new ConfigForm());
            }
            else
            {
                TrayApp.Start();
                Application.Run();
            }
        }
    }
}