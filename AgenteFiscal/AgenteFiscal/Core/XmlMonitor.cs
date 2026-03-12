using System.IO;
using System.Threading.Tasks;
using AgenteFiscal.Utils;

namespace AgenteFiscal.Core
{
    public class XmlMonitor
    {
        FileSystemWatcher watcher;

        public void Start(string path)
        {
            watcher = new FileSystemWatcher();

            watcher.Path = path;
            watcher.Filter = "*.xml";
            watcher.NotifyFilter = NotifyFilters.FileName | NotifyFilters.LastWrite;

            watcher.Created += OnCreated;

            watcher.EnableRaisingEvents = true;

            Logger.Log("Monitorando pasta: " + path);
        }

        private async void OnCreated(object sender, FileSystemEventArgs e)
        {
            try
            {
                await Task.Delay(1500);

                Logger.Log("XML detectado: " + e.FullPath);

                await ApiClient.SendXml(e.FullPath);
            }
            catch (System.Exception ex)
            {
                Logger.Log("Erro monitor: " + ex.Message);
            }
        }
    }
}