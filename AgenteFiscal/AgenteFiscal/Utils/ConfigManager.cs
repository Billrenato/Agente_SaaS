using System;
using System.IO;
using Newtonsoft.Json;

namespace AgenteFiscal.Utils
{
    public class Config
    {
        public string CNPJ { get; set; }
        public string Token { get; set; }
        public string ApiUrl { get; set; }
        public string XmlPath { get; set; }
    }

    public static class ConfigManager
    {
        static string basePath = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            "AgenteFiscal"
        );

        static string configPath = Path.Combine(basePath, "config.json");

        public static bool Exists()
        {
            return File.Exists(configPath);
        }

        public static Config Load()
        {
            var json = File.ReadAllText(configPath);
            return JsonConvert.DeserializeObject<Config>(json);
        }

        public static void Save(Config config)
        {
            Directory.CreateDirectory(basePath);

            var json = JsonConvert.SerializeObject(config, Formatting.Indented);

            File.WriteAllText(configPath, json);
        }
    }
}