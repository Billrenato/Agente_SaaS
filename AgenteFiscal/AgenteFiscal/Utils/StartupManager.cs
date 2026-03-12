using Microsoft.Win32;
using System.Windows.Forms;

namespace AgenteFiscal.Utils
{
    public static class StartupManager
    {
        public static void Add()
        {
            string exe = Application.ExecutablePath;

            RegistryKey key = Registry.CurrentUser.OpenSubKey(
                @"Software\Microsoft\Windows\CurrentVersion\Run",
                true
            );

            key.SetValue("AgenteFiscal", exe);
        }
    }
}