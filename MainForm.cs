using System.Globalization;

namespace RetroRewindToolkit;

internal sealed class MainForm : Form
{
    readonly Color BG=Color.FromArgb(23,25,29), HEADER=Color.FromArgb(16,18,22),
        PANEL=Color.FromArgb(36,39,45), PANEL_ALT=Color.FromArgb(44,48,55),
        BORDER=Color.FromArgb(71,76,85), CREAM=Color.FromArgb(242,229,196),
        MUTED=Color.FromArgb(170,167,159), RED=Color.FromArgb(217,83,79),
        TEAL=Color.FromArgb(67,166,161), GOLD=Color.FromArgb(215,170,82),
        ENTRY=Color.FromArgb(18,20,25), WHITE=Color.FromArgb(247,244,235);

    readonly ComboBox language=new(), savesBox=new();
    readonly TextBox folder=new(), moneyInput=new(), levelInput=new();
    readonly Label langLabel=new(), warning=new(), detected=new(),
        currentMoneyCaption=new(), currentMoneyValue=new(), currentLevelCaption=new(), currentLevelValue=new(),
        saveTitle=new(), folderLabel=new(), saveLabel=new(),
        tutorialMicro=new(), tutorialTitle=new(),
        moneyMicro=new(), moneyTitle=new(), amountLabel=new(), moneyNote=new(),
        levelMicro=new(), levelTitle=new(), levelNote=new(), newLevelLabel=new(),
        statusLabel=new();
    readonly Button browse=new(), refresh=new(), skip=new(), changeMoney=new(), changeLevel=new();
    List<SaveInfo> saves=new();

    string Lang => language.SelectedItem?.ToString() ?? "Español";
    string Tr(string k) => T.Text[Lang][k];
    string Fmt(string k, params (string key,string value)[] values)
    {
        string s=Tr(k);
        foreach(var v in values) s=s.Replace("{"+v.key+"}",v.value);
        return s;
    }

    public MainForm()
    {
        Text="Retro Rewind Toolkit";
        StartPosition=FormStartPosition.CenterScreen;
        ClientSize=new Size(900,900);
        MinimumSize=new Size(840,900);
        BackColor=BG; ForeColor=CREAM;
        Font=new Font("Segoe UI",9F);
        Build();
        folder.Text=SaveOps.DefaultSaveDirectory();
        language.SelectedItem="Español";
        Translate();
        RefreshSaves();
    }

    void Build()
    {
        // Root layout: fixed header row + body row.
        // This avoids Dock.Fill rendering underneath the header.
        var root=new TableLayoutPanel
        {
            Dock=DockStyle.Fill,
            BackColor=BG,
            ColumnCount=1,
            RowCount=2,
            Margin=new Padding(0),
            Padding=new Padding(0)
        };
        root.ColumnStyles.Add(new ColumnStyle(SizeType.Percent,100));
        root.RowStyles.Add(new RowStyle(SizeType.Absolute,132));
        root.RowStyles.Add(new RowStyle(SizeType.Percent,100));
        Controls.Add(root);

        var header=new TableLayoutPanel
        {
            Dock=DockStyle.Fill,BackColor=HEADER,
            ColumnCount=2,RowCount=1,Padding=new Padding(28,12,28,10),
            Margin=new Padding(0)
        };
        header.ColumnStyles.Add(new ColumnStyle(SizeType.Percent,70));
        header.ColumnStyles.Add(new ColumnStyle(SizeType.Percent,30));
        root.Controls.Add(header,0,0);

        var brand=new FlowLayoutPanel
        {
            Dock=DockStyle.Fill,FlowDirection=FlowDirection.TopDown,WrapContents=false,
            BackColor=HEADER,Margin=new Padding(0)
        };
        brand.Controls.Add(new Label{AutoSize=true,Text="RETRO REWIND",ForeColor=CREAM,
            Font=new Font("Segoe UI",23,FontStyle.Bold),Margin=new Padding(0,2,0,0)});
        brand.Controls.Add(new Label{AutoSize=true,Text="TOOLKIT",ForeColor=RED,
            Font=new Font("Consolas",13,FontStyle.Bold),Margin=new Padding(2,0,0,0)});
        header.Controls.Add(brand,0,0);

        var langPanel=new TableLayoutPanel
        {
            Dock=DockStyle.Fill,BackColor=HEADER,RowCount=2,ColumnCount=1,Margin=new Padding(0),
            Padding=new Padding(0,4,0,0)
        };
        langPanel.RowStyles.Add(new RowStyle(SizeType.Absolute,26));
        langPanel.RowStyles.Add(new RowStyle(SizeType.Absolute,34));
        langLabel.Dock=DockStyle.Fill;
        langLabel.TextAlign=ContentAlignment.BottomRight;
        langLabel.ForeColor=MUTED;
        langPanel.Controls.Add(langLabel,0,0);

        language.DropDownStyle=ComboBoxStyle.DropDownList;
        language.Items.AddRange(new object[]{"Español","English","Français","Deutsch","Italiano","Português"});
        language.Width=145;
        language.Anchor=AnchorStyles.Top|AnchorStyles.Right;
        language.SelectedIndexChanged+=(_,_)=>{Translate();RefreshSaves();};
        langPanel.Controls.Add(language,0,1);
        header.Controls.Add(langPanel,1,0);

        var body=new TableLayoutPanel
        {
            Dock=DockStyle.Fill,BackColor=BG,Padding=new Padding(26,12,26,10),
            ColumnCount=1,RowCount=6,Margin=new Padding(0)
        };
        body.ColumnStyles.Add(new ColumnStyle(SizeType.Percent,100));
        body.RowStyles.Add(new RowStyle(SizeType.Absolute,48));
        body.RowStyles.Add(new RowStyle(SizeType.Absolute,210));
        body.RowStyles.Add(new RowStyle(SizeType.Absolute,118));
        body.RowStyles.Add(new RowStyle(SizeType.Absolute,148));
        body.RowStyles.Add(new RowStyle(SizeType.Absolute,148));
        body.RowStyles.Add(new RowStyle(SizeType.Percent,100));
        root.Controls.Add(body,0,1);

        warning.Dock=DockStyle.Fill;
        warning.Margin=new Padding(0,0,0,10);
        warning.BackColor=GOLD;
        warning.ForeColor=Color.FromArgb(24,24,24);
        warning.TextAlign=ContentAlignment.MiddleCenter;
        warning.Font=new Font("Segoe UI",10,FontStyle.Bold);
        body.Controls.Add(warning,0,0);

        body.Controls.Add(BuildSaveCard(),0,1);
        body.Controls.Add(BuildTutorialCard(),0,2);
        body.Controls.Add(BuildMoneyCard(),0,3);
        body.Controls.Add(BuildLevelCard(),0,4);

        var footer=new Panel{Dock=DockStyle.Fill,BackColor=BG,Margin=new Padding(0,7,0,0)};
        statusLabel.AutoSize=true;
        statusLabel.ForeColor=MUTED;
        statusLabel.Font=new Font("Segoe UI",8);
        statusLabel.Location=new Point(0,5);
        footer.Controls.Add(statusLabel);
        body.Controls.Add(footer,0,5);
    }

    Control BuildSaveCard()
    {
        var inner=InnerCard(out var outer);
        outer.Margin=new Padding(0,0,0,10);

        var grid=new TableLayoutPanel{Dock=DockStyle.Fill,ColumnCount=1,RowCount=4,Padding=new Padding(16,10,16,10),BackColor=PANEL};
        grid.RowStyles.Add(new RowStyle(SizeType.Absolute,38));
        grid.RowStyles.Add(new RowStyle(SizeType.Absolute,48));
        grid.RowStyles.Add(new RowStyle(SizeType.Absolute,48));
        grid.RowStyles.Add(new RowStyle(SizeType.Absolute,42));
        inner.Controls.Add(grid);

        var top=new TableLayoutPanel{Dock=DockStyle.Fill,ColumnCount=2,BackColor=PANEL};
        top.ColumnStyles.Add(new ColumnStyle(SizeType.Percent,55)); top.ColumnStyles.Add(new ColumnStyle(SizeType.Percent,45));
        var left=new FlowLayoutPanel{Dock=DockStyle.Fill,BackColor=PANEL,FlowDirection=FlowDirection.LeftToRight,WrapContents=false};
        left.Controls.Add(new Label{AutoSize=true,Text="▰",ForeColor=TEAL,BackColor=PANEL,Font=new Font("Segoe UI",13,FontStyle.Bold),Margin=new Padding(0,3,5,0)});
        saveTitle.AutoSize=true;saveTitle.ForeColor=CREAM;saveTitle.BackColor=PANEL;saveTitle.Font=new Font("Segoe UI",11,FontStyle.Bold);saveTitle.Margin=new Padding(0,5,0,0);
        left.Controls.Add(saveTitle);
        detected.Dock=DockStyle.Fill;detected.TextAlign=ContentAlignment.MiddleRight;detected.ForeColor=TEAL;detected.BackColor=PANEL;
        top.Controls.Add(left,0,0);top.Controls.Add(detected,1,0);grid.Controls.Add(top,0,0);

        grid.Controls.Add(FormRow(folderLabel,folder,browse),0,1);
        grid.Controls.Add(FormRow(saveLabel,savesBox,refresh),0,2);

        var current=new FlowLayoutPanel{Dock=DockStyle.Fill,BackColor=PANEL,FlowDirection=FlowDirection.LeftToRight,WrapContents=false,Padding=new Padding(0,6,0,0)};
        currentMoneyCaption.AutoSize=true;currentMoneyCaption.ForeColor=MUTED;currentMoneyCaption.Font=new Font("Segoe UI",9,FontStyle.Bold);
        currentMoneyValue.AutoSize=true;currentMoneyValue.ForeColor=TEAL;currentMoneyValue.Font=new Font("Consolas",10,FontStyle.Bold);currentMoneyValue.Margin=new Padding(6,0,22,0);
        currentLevelCaption.AutoSize=true;currentLevelCaption.ForeColor=MUTED;currentLevelCaption.Font=new Font("Segoe UI",9,FontStyle.Bold);
        currentLevelValue.AutoSize=true;currentLevelValue.ForeColor=GOLD;currentLevelValue.Font=new Font("Consolas",10,FontStyle.Bold);currentLevelValue.Margin=new Padding(6,0,0,0);
        current.Controls.AddRange(new Control[]{currentMoneyCaption,currentMoneyValue,currentLevelCaption,currentLevelValue});
        grid.Controls.Add(current,0,3);

        browse.Click+=Browse;
        refresh.Click+=(_,_)=>RefreshSaves();
        savesBox.SelectedIndexChanged+=(_,_)=>ShowSelected();
        return outer;
    }

    Control FormRow(Label caption, Control field, Button button)
    {
        var row=new TableLayoutPanel{Dock=DockStyle.Fill,BackColor=PANEL,ColumnCount=3,Margin=new Padding(0)};
        row.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute,145));
        row.ColumnStyles.Add(new ColumnStyle(SizeType.Percent,100));
        row.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute,120));
        caption.Dock=DockStyle.Fill;caption.TextAlign=ContentAlignment.MiddleLeft;caption.ForeColor=MUTED;
        field.Dock=DockStyle.Fill;field.Margin=new Padding(0,6,8,6);
        button.Dock=DockStyle.Fill;button.Margin=new Padding(0,5,0,5);StyleButton(button,TEAL);
        row.Controls.Add(caption,0,0);row.Controls.Add(field,1,0);row.Controls.Add(button,2,0);
        if(field is TextBox tb) StyleText(tb);
        if(field is ComboBox cb){cb.DropDownStyle=ComboBoxStyle.DropDownList;cb.BackColor=ENTRY;cb.ForeColor=WHITE;}
        return row;
    }

    Control BuildTutorialCard()
    {
        var content=ToolCard(RED,tutorialMicro,tutorialTitle,out var outer);
        outer.Margin=new Padding(0,0,0,8);
        skip.AutoSize=true;skip.MinimumSize=new Size(155,36);StyleButton(skip,RED);
        skip.Click+=SkipTutorial; content.Controls.Add(skip);
        return outer;
    }

    Control BuildMoneyCard()
    {
        var content=ToolCard(TEAL,moneyMicro,moneyTitle,out var outer);
        outer.Margin=new Padding(0,0,0,8);
        moneyNote.AutoSize=true;moneyNote.MaximumSize=new Size(760,0);moneyNote.ForeColor=GOLD;moneyNote.Font=new Font("Segoe UI",8,FontStyle.Bold);moneyNote.Margin=new Padding(0,2,0,5);
        content.Controls.Add(moneyNote);
        var row=new FlowLayoutPanel{AutoSize=true,FlowDirection=FlowDirection.LeftToRight,WrapContents=false,BackColor=PANEL,Margin=new Padding(0,6,0,0)};
        amountLabel.AutoSize=true;amountLabel.ForeColor=MUTED;amountLabel.Margin=new Padding(0,8,10,0);
        moneyInput.Width=150;StyleText(moneyInput);moneyInput.Margin=new Padding(0,4,10,0);
        changeMoney.AutoSize=true;changeMoney.MinimumSize=new Size(145,36);StyleButton(changeMoney,TEAL);
        changeMoney.Click+=ChangeMoney;
        row.Controls.AddRange(new Control[]{amountLabel,moneyInput,changeMoney});
        content.Controls.Add(row);
        return outer;
    }

    Control BuildLevelCard()
    {
        var content=ToolCard(GOLD,levelMicro,levelTitle,out var outer);
        outer.Margin=new Padding(0,0,0,8);
        levelNote.AutoSize=true;levelNote.MaximumSize=new Size(760,0);levelNote.ForeColor=GOLD;levelNote.Font=new Font("Segoe UI",8,FontStyle.Bold);levelNote.Margin=new Padding(0,2,0,7);
        content.Controls.Add(levelNote);
        var row=new FlowLayoutPanel{AutoSize=true,FlowDirection=FlowDirection.LeftToRight,WrapContents=false,BackColor=PANEL,Margin=new Padding(0)};
        newLevelLabel.AutoSize=true;newLevelLabel.ForeColor=MUTED;newLevelLabel.Margin=new Padding(0,8,10,0);
        levelInput.Width=150;StyleText(levelInput);levelInput.Margin=new Padding(0,4,10,0);
        changeLevel.AutoSize=true;changeLevel.MinimumSize=new Size(145,36);StyleButton(changeLevel,TEAL);
        changeLevel.Click+=ChangeLevel;
        row.Controls.AddRange(new Control[]{newLevelLabel,levelInput,changeLevel});
        content.Controls.Add(row);
        return outer;
    }

    FlowLayoutPanel ToolCard(Color stripeColor, Label micro, Label title, out Panel outer)
    {
        var inner=InnerCard(out outer);
        var stripe=new Panel{Dock=DockStyle.Left,Width=7,BackColor=stripeColor};inner.Controls.Add(stripe);
        var content=new FlowLayoutPanel
        {
            Dock=DockStyle.Fill,FlowDirection=FlowDirection.TopDown,WrapContents=false,
            BackColor=PANEL,Padding=new Padding(16,11,12,8)
        };
        micro.AutoSize=true;micro.ForeColor=stripeColor;micro.BackColor=PANEL;micro.Font=new Font("Consolas",9,FontStyle.Bold);micro.Margin=new Padding(0,0,0,0);
        title.AutoSize=true;title.ForeColor=CREAM;title.BackColor=PANEL;title.Font=new Font("Segoe UI",12,FontStyle.Bold);title.Margin=new Padding(0,2,0,4);
        content.Controls.Add(micro);content.Controls.Add(title);inner.Controls.Add(content);
        content.BringToFront();
        return content;
    }

    Panel InnerCard(out Panel outer)
    {
        outer=new Panel{Dock=DockStyle.Fill,BackColor=BORDER,Padding=new Padding(1)};
        var inner=new Panel{Dock=DockStyle.Fill,BackColor=PANEL};outer.Controls.Add(inner);return inner;
    }

    void StyleButton(Button b,Color c)
    {
        b.FlatStyle=FlatStyle.Flat;b.FlatAppearance.BorderSize=0;b.BackColor=c;b.ForeColor=WHITE;
        b.Font=new Font("Segoe UI",9,FontStyle.Bold);b.Cursor=Cursors.Hand;
    }
    void StyleText(TextBox t)
    {
        t.BackColor=ENTRY;t.ForeColor=WHITE;t.BorderStyle=BorderStyle.FixedSingle;t.Font=new Font("Segoe UI",10);
    }

    void Translate()
    {
        if(language.SelectedIndex<0)return;
        langLabel.Text=Tr("lang");warning.Text=Tr("warning");
        saveTitle.Text=Tr("save");folderLabel.Text=Tr("folder");browse.Text=Tr("browse");saveLabel.Text=Tr("save");refresh.Text=Tr("refresh");
        currentMoneyCaption.Text=Tr("current_money");currentLevelCaption.Text=Tr("current_level");
        tutorialMicro.Text="▣  "+Tr("vhs_label");tutorialTitle.Text=Tr("tutorial");skip.Text=Tr("skip");
        moneyMicro.Text="$  "+Tr("cash_label");moneyTitle.Text=Tr("money");moneyNote.Text=Tr("money_note");amountLabel.Text=Tr("amount");changeMoney.Text=Tr("change_money");
        levelMicro.Text="★  "+Tr("progress_label");levelTitle.Text=Tr("level")+" *";newLevelLabel.Text=Tr("new_level");changeLevel.Text=Tr("change_level");levelNote.Text=Tr("level_note");
        statusLabel.Text="● Offline   •   Automatic backups   •   No administrator rights required";
        ShowSelected();
    }

    void Browse(object? s,EventArgs e)
    {
        using var d=new FolderBrowserDialog{SelectedPath=Directory.Exists(folder.Text)?folder.Text:""};
        if(d.ShowDialog(this)==DialogResult.OK){folder.Text=d.SelectedPath;RefreshSaves();}
    }

    void RefreshSaves()
    {
        saves=SaveOps.ReadSaves(folder.Text.Trim());
        string? previous=savesBox.SelectedItem?.ToString();
        savesBox.Items.Clear();
        foreach(var s in saves)savesBox.Items.Add(s.DisplayName);
        detected.Text=saves.Count>0?Fmt("found",("n",saves.Count.ToString())):Tr("none");
        detected.ForeColor=saves.Count>0?TEAL:RED;
        if(saves.Count>0)
        {
            int idx=previous!=null?savesBox.Items.IndexOf(previous):-1;
            savesBox.SelectedIndex=idx>=0?idx:0;
        }
        else ShowSelected();
    }

    SaveInfo? Selected()=>savesBox.SelectedIndex>=0&&savesBox.SelectedIndex<saves.Count?saves[savesBox.SelectedIndex]:null;

    void ShowSelected()
    {
        if(language.SelectedIndex<0)return;
        var s=Selected();
        if(s==null)
        {
            currentMoneyValue.Text="—";currentLevelValue.Text="—";changeLevel.Enabled=false;return;
        }
        currentMoneyValue.Text=s.Money.HasValue?"$"+s.Money.Value.ToString("#,##0.00",CultureInfo.InvariantCulture):"—";
        currentLevelValue.Text=s.StoreLevel.HasValue?s.StoreLevel.Value.ToString():Tr("level_zero");
        changeLevel.Enabled=s.StoreLevel.HasValue&&s.StoreLevel.Value>=1;
    }

    bool Confirm(string message)=>MessageBox.Show(this,message,Tr("confirm"),MessageBoxButtons.YesNo,MessageBoxIcon.Warning)==DialogResult.Yes;

    void SkipTutorial(object? a,EventArgs b)
    {
        var s=Selected();if(s==null){MessageBox.Show(this,Tr("select"),Tr("error"));return;}
        string q=Fmt("skip_confirm",("label",s.DisplayName));
        if(!Confirm(q))return;
        try{
            var r=SaveOps.SkipTutorial(s.FilePath);
            string msg=r.Status=="already"?Tr("skip_already"):Tr("skip_done")+(r.BackupPath!=null?"\n\n"+Tr("backup")+" "+r.BackupPath:"");
            MessageBox.Show(this,msg,Tr("done"),MessageBoxButtons.OK,MessageBoxIcon.Information);RefreshSaves();
        }catch(Exception ex){MessageBox.Show(this,ex.Message,Tr("error"),MessageBoxButtons.OK,MessageBoxIcon.Error);}
    }

    void ChangeMoney(object? a,EventArgs b)
    {
        var s=Selected();if(s==null){MessageBox.Show(this,Tr("select"),Tr("error"));return;}
        string raw=moneyInput.Text.Trim().Replace(',','.');
        if(!decimal.TryParse(raw,NumberStyles.Number,CultureInfo.InvariantCulture,out var value)){MessageBox.Show(this,Tr("money_invalid"),Tr("error"));return;}
        if(value<0){MessageBox.Show(this,Tr("money_negative"),Tr("error"));return;}
        string shown="$"+value.ToString("#,##0.00",CultureInfo.InvariantCulture);
        if(!Confirm(Fmt("money_confirm",("label",s.DisplayName),("shown",shown))))return;
        try{
            string backup=SaveOps.SetMoney(s.FilePath,value);
            MessageBox.Show(this,Fmt("money_done",("shown",shown))+"\n\n"+Tr("backup")+" "+backup,Tr("done"),MessageBoxButtons.OK,MessageBoxIcon.Information);
            RefreshSaves();
        }catch(Exception ex){MessageBox.Show(this,ex.Message,Tr("error"),MessageBoxButtons.OK,MessageBoxIcon.Error);}
    }

    void ChangeLevel(object? a,EventArgs b)
    {
        var s=Selected();if(s==null){MessageBox.Show(this,Tr("select"),Tr("error"));return;}
        if(!int.TryParse(levelInput.Text.Trim(),out int level)){MessageBox.Show(this,Tr("level_invalid"),Tr("error"));return;}
        if(level<1){MessageBox.Show(this,Tr("level_min"),Tr("error"));return;}
        if(!Confirm(Fmt("level_confirm",("label",s.DisplayName),("level",level.ToString()))))return;
        try{
            var r=SaveOps.SetStoreLevel(s.FilePath,level);
            MessageBox.Show(this,Fmt("level_done",("old",r.OldLevel.ToString()),("new",level.ToString()))+"\n\n"+Tr("backup")+" "+r.BackupPath,Tr("done"),MessageBoxButtons.OK,MessageBoxIcon.Information);
            RefreshSaves();
        }catch(Exception ex){MessageBox.Show(this,ex.Message,Tr("error"),MessageBoxButtons.OK,MessageBoxIcon.Error);}
    }
}
