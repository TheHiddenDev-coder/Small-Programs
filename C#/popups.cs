using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Windows.Forms;

namespace JokePopups
{
    static class Program
    {
        // Store all popups to allow "Close All"
        static List<Form> popups = new List<Form>();

        [STAThread]
        static void Main()
        {
            int numOfPopups = 500;
            
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            string[] messages = new string[]
            {
                "System32.dll not found.",
                "Fatal Exception 0x80004005.",
                "Critical memory leak detected.",
                "Unexpected success error.",
                "User competence not recognized.",
                "Error: Teacher is smarter than you thought.",
                "Access Denied: Brain locked.",
                "Password 12345… just kidding!"
            };

            Random rand = new Random();

            // Spawn multiple popups
            for (int i = 0; i < numOfPopups; i++)
            {
                Form popup = new Form();
                popup.StartPosition = FormStartPosition.Manual;
                popup.Location = new Point(rand.Next(0, 800), rand.Next(0, 500));
                popup.Size = new Size(350, 150);
                popup.Text = "Critical System Error";
                popup.TopMost = true;

                Label lbl = new Label();
                lbl.Text = messages[rand.Next(messages.Length)];
                lbl.AutoSize = true;
                lbl.Location = new Point(30, 40);
                popup.Controls.Add(lbl);

                popups.Add(popup);

                // Show without blocking
                popup.Show();
            }

            // Final "Close All" window
            Form closeAllForm = new Form();
            closeAllForm.StartPosition = FormStartPosition.CenterScreen;
            closeAllForm.Size = new Size(400, 200);
            closeAllForm.Text = "SYSTEM FAILURE";
            closeAllForm.TopMost = true;

            Button btnCloseAll = new Button();
            btnCloseAll.Text = "Close All Errors";
            btnCloseAll.Size = new Size(200, 50);
            btnCloseAll.Location = new Point(100, 80);
            btnCloseAll.Click += (s, e) =>
            {
                foreach (var f in popups)
                {
                    if (!f.IsDisposed)
                        f.Close();
                }
                closeAllForm.Close();
            };

            closeAllForm.Controls.Add(btnCloseAll);

            Application.Run(closeAllForm);
        }
    }
}
