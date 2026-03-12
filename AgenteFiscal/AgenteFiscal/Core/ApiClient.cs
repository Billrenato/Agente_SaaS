using System.IO;
using System.Net.Http;
using System.Threading.Tasks;
using AgenteFiscal.Utils;

namespace AgenteFiscal.Core
{
    public static class ApiClient
    {
        public static async Task SendXml(string filePath)
        {
            try
            {
                var config = ConfigManager.Load();

                using var client = new HttpClient();

                client.DefaultRequestHeaders.Add("Authorization", "Bearer " + config.Token);

                var content = new MultipartFormDataContent();

                content.Add(new StringContent(config.CNPJ), "cnpj");

                var fileBytes = File.ReadAllBytes(filePath);

                content.Add(new ByteArrayContent(fileBytes), "arquivo", Path.GetFileName(filePath));

                var response = await client.PostAsync(config.ApiUrl, content);

                if (response.IsSuccessStatusCode)
                {
                    Logger.Log("XML enviado: " + Path.GetFileName(filePath));
                }
                else
                {
                    Logger.Log("Erro envio API: " + response.StatusCode);
                }
            }
            catch (System.Exception ex)
            {
                Logger.Log("Erro envio: " + ex.Message);
            }
        }
    }
}