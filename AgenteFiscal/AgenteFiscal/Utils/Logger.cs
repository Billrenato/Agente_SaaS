using System;
using System.IO;

namespace AgenteFiscal.Utils
{
    public static class Logger
    {
        static string logPath = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            "AgenteFiscal",
            "logs.txt"
        );

        public static void Log(string message)
        {
            Directory.CreateDirectory(Path.GetDirectoryName(logPath));

            string line = DateTime.Now + " - " + message + Environment.NewLine;

            File.AppendAllText(logPath, line);
        }
    }
}