using System;
using System.Windows.Forms;
using AgenteFiscal.Utils;

namespace AgenteFiscal.UI
{
    public class ConfigForm : Form
    {
        TextBox txtCnpj = new TextBox();
        TextBox txtToken = new TextBox();
        TextBox txtApi = new TextBox();
        TextBox txtPath = new TextBox();

        Button btnSalvar = new Button();
        Button btnPasta = new Button();

        FolderBrowserDialog folderDialog = new FolderBrowserDialog();

        public ConfigForm()
        {
            Text = "Configuração Agente Fiscal";

            Width = 420;
            Height = 300;

            Label l1 = new Label() { Text = "CNPJ", Top = 20, Left = 20 };
            txtCnpj.SetBounds(20, 40, 350, 25);

            Label l2 = new Label() { Text = "Token API", Top = 70, Left = 20 };
            txtToken.SetBounds(20, 90, 350, 25);

            Label l3 = new Label() { Text = "API URL", Top = 120, Left = 20 };
            txtApi.SetBounds(20, 140, 350, 25);

            Label l4 = new Label() { Text = "Pasta XML", Top = 170, Left = 20 };
            txtPath.SetBounds(20, 190, 250, 25);

            btnPasta.Text = "...";
            btnPasta.SetBounds(280, 190, 40, 25);
            btnPasta.Click += EscolherPasta;

            btnSalvar.Text = "Salvar";
            btnSalvar.SetBounds(20, 220, 100, 30);
            btnSalvar.Click += Salvar;

            Controls.AddRange(new Control[] {
                l1, txtCnpj,
                l2, txtToken,
                l3, txtApi,
                l4, txtPath,
                btnPasta,
                btnSalvar
            });
        }

        void EscolherPasta(object sender, EventArgs e)
        {
            if (folderDialog.ShowDialog() == DialogResult.OK)
            {
                txtPath.Text = folderDialog.SelectedPath;
            }
        }

        void Salvar(object sender, EventArgs e)
        {
            try
            {
                Config config = new Config();

                config.CNPJ = txtCnpj.Text;
                config.Token = txtToken.Text;
                config.ApiUrl = txtApi.Text;
                config.XmlPath = txtPath.Text;

                ConfigManager.Save(config);

                StartupManager.Add();

                MessageBox.Show("Configuração salva com sucesso!");

                Application.Exit();
            }
            catch (Exception ex)
            {
                MessageBox.Show("Erro: " + ex.Message);
            }
        }
    }
}
