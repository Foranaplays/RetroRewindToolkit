using System.Buffers.Binary;
using System.Text;
using System.Text.RegularExpressions;

namespace RetroRewindToolkit;

internal sealed record SaveInfo(
    string FilePath,
    string FileName,
    string? StoreName,
    decimal? Money,
    int? StoreLevel,
    DateTime ModifiedUtc)
{
    public string DisplayName => string.IsNullOrWhiteSpace(StoreName)
        ? FileName
        : $"{StoreName} — {FileName}";
}

internal static class SaveOps
{
    private static readonly byte[] Money64Name =
        Encoding.ASCII.GetBytes("Money64_14_4E3C8A914A3F4058F90C30BD533FEF7E\0");
    private static readonly byte[] Money64Prop = Encoding.ASCII.GetBytes("Int64Property\0");
    private static readonly byte[] Money32Name =
        Encoding.ASCII.GetBytes("Money_2_334F50394D552F37FAADAB9A3C50D7D7\0");
    private static readonly byte[] LevelName =
        Encoding.ASCII.GetBytes("Level_4_D665A6394BEDE281DFD626929A94188A\0");
    private static readonly byte[] IntProp = Encoding.ASCII.GetBytes("IntProperty\0");
    private static readonly byte[] TextProperty = Encoding.ASCII.GetBytes("TextProperty\0");

    private static readonly byte[] QuestMarker = Encoding.ASCII.GetBytes("Quest\0");
    private static readonly byte[] StatisticMarker = Encoding.ASCII.GetBytes("Statistic\0");
    private static readonly byte[] EndTutorial = Encoding.ASCII.GetBytes("Quest_EndTutorial-Basic");

    private const string TutorialPatchB64 = "BgAAAFF1ZXN0AA4AAABBcnJheVByb3BlcnR5AAEAAAAPAAAAU3RydWN0UHJvcGVydHkAAgAAAA0AAABRdWVzdF9TdHJ1Y3QAAQAAADMAAAAvR2FtZS9WaWRlb1N0b3JlL2NvcmUvYmx1ZXByaW50L3F1ZXN0L1F1ZXN0X1N0cnVjdAAAAAAAJQAAADE3MTY2MTRlLTRjNzItZmI5Ni0xYzJlLWZkYWNlNTdhMGQ3MQAAAAAArgEAAAABAAAAJgAAAElEXzhfNDcyNjkzQkM0NDg2QTczNzM0REE0MEEwMzFBRTkzNTkADwAAAFN0cnVjdFByb3BlcnR5AAEAAAAFAAAAR3VpZAABAAAAFAAAAC9TY3JpcHQvQ29yZVVPYmplY3QAAAAAABAAAAAIFH7ZBfcy/UKTaGQz7nsNgi8AAABRdWVzdENsYXNzXzExX0NFNUNFNjY1NEFBMjY3RTY2MTQwNzdBMTAxODcxRDMxAA8AAABPYmplY3RQcm9wZXJ0eQAAAAAAgwAAAAB/AAAAL0dhbWUvVmlkZW9TdG9yZS9jb3JlL2JsdWVwcmludC9xdWVzdC9UdXRvcmlhbC9RdWVzdF9SZXR1cm5Cb3gtU2NhblJldHVybk1vdmllX0Jyb2tlbi5RdWVzdF9SZXR1cm5Cb3gtU2NhblJldHVybk1vdmllX0Jyb2tlbl9DAC8AAABQcm9ncmVzc2lvbl82XzIxRTg2MUU0NEM1RERCQ0VBQ0YzRjQ5NTYwOTdFRUUxAAwAAABJbnRQcm9wZXJ0eQAAAAAABAAAAAAAAAAABQAAAE5vbmUADQAAAFF1ZXN0TWFuYWdlcgAPAAAAU3RydWN0UHJvcGVydHkAAgAAABMAAABRdWVzdF9NYW5hZ2VyX1NhdmUAAQAAADkAAAAvR2FtZS9WaWRlb1N0b3JlL2NvcmUvYmx1ZXByaW50L3F1ZXN0L1F1ZXN0X01hbmFnZXJfU2F2ZQAAAAAAJQAAAGMzZDRjNzFjLTRhZDUtNGMyMS0yMTYyLTA2OGJiZjFlNjg2MgAAAAAARwoAAAAtAAAAUXVlc3REb25lXzRfNTIyNEY5MjI0MjhDQTVERkE3RTg2QjlFRDhFODhEOTAADAAAAE1hcFByb3BlcnR5AAIAAAAPAAAAT2JqZWN0UHJvcGVydHkAAAAAAA0AAABCb29sUHJvcGVydHkAAAAAAMgJAAAAAAAAABkAAABTAAAAL0dhbWUvVmlkZW9TdG9yZS9jb3JlL2JsdWVwcmludC9xdWVzdC9UdXRvcmlhbC9RdWVzdF9Nb3ZlUGxheWVyLlF1ZXN0X01vdmVQbGF5ZXJfQwABXQAAAC9HYW1lL1ZpZGVvU3RvcmUvY29yZS9ibHVlcHJpbnQvcXVlc3QvVHV0b3JpYWwvUXVlc3RfQWNjZXNzQ2F0YWxvZ3VlLlF1ZXN0X0FjY2Vzc0NhdGFsb2d1ZV9DAAFTAAAAL0dhbWUvVmlkZW9TdG9yZS9jb3JlL2JsdWVwcmludC9xdWVzdC9UdXRvcmlhbC9RdWVzdF9CdXlTaGVsdmVzLlF1ZXN0X0J1eVNoZWx2ZXNfQwABWQAAAC9HYW1lL1ZpZGVvU3RvcmUvY29yZS9ibHVlcHJpbnQvcXVlc3QvVHV0b3JpYWwvUXVlc3RfUGlja1VwU2hlbHZlcy5RdWVzdF9QaWNrVXBTaGVsdmVzX0MAAVcAAAAvR2FtZS9WaWRlb1N0b3JlL2NvcmUvYmx1ZXByaW50L3F1ZXN0L1R1dG9yaWFsL1F1ZXN0X1BsYWNlU2hlbHZlcy5RdWVzdF9QbGFjZVNoZWx2ZXNfQwABWwAAAC9HYW1lL1ZpZGVvU3RvcmUvY29yZS9ibHVlcHJpbnQvcXVlc3QvVHV0b3JpYWwvUXVlc3RfQWNjZXNzQ29tcHV0ZXIuUXVlc3RfQWNjZXNzQ29tcHV0ZXJfQwABUQAAAC9HYW1lL1ZpZGVvU3RvcmUvY29yZS9ibHVlcHJpbnQvcXVlc3QvVHV0b3JpYWwvUXVlc3RfQnV5TW92aWVzLlF1ZXN0X0J1eU1vdmllc19DAAFXAAAAL0dhbWUvVmlkZW9TdG9yZS9jb3JlL2JsdWVwcmludC9xdWVzdC9UdXRvcmlhbC9RdWVzdF9QaWNrVXBNb3ZpZXMuUXVlc3RfUGlja1VwTW92aWVzX0MAAWcAAAAvR2FtZS9WaWRlb1N0b3JlL2NvcmUvYmx1ZXByaW50L3F1ZXN0L1R1dG9yaWFsL1F1ZXN0X1N0b2NrTW92aWVzSW5TaGVsdmVzLlF1ZXN0X1N0b2NrTW92aWVzSW5TaGVsdmVzX0MAAU8AAAAvR2FtZS9WaWRlb1N0b3JlL2NvcmUvYmx1ZXByaW50L3F1ZXN0L1R1dG9yaWFsL1F1ZXN0X1NhdmVHYW1lLlF1ZXN0X1NhdmVHYW1lX0MAAV0AAAAvR2FtZS9WaWRlb1N0b3JlL2NvcmUvYmx1ZXByaW50L3F1ZXN0L1R1dG9yaWFsL1F1ZXN0X0FjY2Vzc05hbWVTdG9yZS5RdWVzdF9BY2Nlc3NOYW1lU3RvcmVfQwABTwAAAC9HYW1lL1ZpZGVvU3RvcmUvY29yZS9ibHVlcHJpbnQvcXVlc3QvVHV0b3JpYWwvUXVlc3RfT3BlblNpZ24uUXVlc3RfT3BlblNpZ25fQwABVwAAAC9HYW1lL1ZpZGVvU3RvcmUvY29yZS9ibHVlcHJpbnQvcXVlc3QvVHV0b3JpYWwvUXVlc3RfQWNjZXNzRmx5ZXJzLlF1ZXN0X0FjY2Vzc0ZseWVyc19DAAFtAAAAL0dhbWUvVmlkZW9TdG9yZS9jb3JlL2JsdWVwcmludC9xdWVzdC9UdXRvcmlhbC9RdWVzdF9DaGVja091dC1TZXJ2ZUN1c3RvbWVycy5RdWVzdF9DaGVja091dC1TZXJ2ZUN1c3RvbWVyc19DAAFbAAAAL0dhbWUvVmlkZW9TdG9yZS9jb3JlL2JsdWVwcmludC9xdWVzdC9UdXRvcmlhbC9RdWVzdF9BY2Nlc3NDYWxlbmRhci5RdWVzdF9BY2Nlc3NDYWxlbmRhcl9DAAFXAAAAL0dhbWUvVmlkZW9TdG9yZS9jb3JlL2JsdWVwcmludC9xdWVzdC9UdXRvcmlhbC9RdWVzdF9BY2Nlc3NSZXR1cm4uUXVlc3RfQWNjZXNzUmV0dXJuX0MAAXMAAAAvR2FtZS9WaWRlb1N0b3JlL2NvcmUvYmx1ZXByaW50L3F1ZXN0L1R1dG9yaWFsL1F1ZXN0X1JldHVybkJveC1TY2FuUmV0dXJuTW92aWVzLlF1ZXN0X1JldHVybkJveC1TY2FuUmV0dXJuTW92aWVzX0MAAWcAAAAvR2FtZS9WaWRlb1N0b3JlL2NvcmUvYmx1ZXByaW50L3F1ZXN0L1R1dG9yaWFsL1F1ZXN0X1N0b2NrLVJlc2VydmVkTW92aWVzLlF1ZXN0X1N0b2NrLVJlc2VydmVkTW92aWVzX0MAAVkAAAAvR2FtZS9WaWRlb1N0b3JlL2NvcmUvYmx1ZXByaW50L3F1ZXN0L1R1dG9yaWFsL1F1ZXN0X09wZW5TaWduLURheTIuUXVlc3RfT3BlblNpZ24tRGF5Ml9DAAFfAAAAL0dhbWUvVmlkZW9TdG9yZS9jb3JlL2JsdWVwcmludC9xdWVzdC9UdXRvcmlhbC9RdWVzdF9BY2Nlc3MtVGVsZXBob25lLlF1ZXN0X0FjY2Vzcy1UZWxlcGhvbmVfQwABhQAAAC9HYW1lL1ZpZGVvU3RvcmUvY29yZS9ibHVlcHJpbnQvcXVlc3QvVHV0b3JpYWwvUXVlc3QtUmVwZWF0YWJsZV9QaG9uZV9QaWNrVXAtUmVzZXJ2YXRpb24uUXVlc3QtUmVwZWF0YWJsZV9QaG9uZV9QaWNrVXAtUmVzZXJ2YXRpb25fQwABZQAAAC9HYW1lL1ZpZGVvU3RvcmUvY29yZS9ibHVlcHJpbnQvcXVlc3QvVHV0b3JpYWwvUXVlc3RfTmV3UmVsZWFzZV9CdXlNb3ZpZS5RdWVzdF9OZXdSZWxlYXNlX0J1eU1vdmllX0MAAXsAAAAvR2FtZS9WaWRlb1N0b3JlL2NvcmUvYmx1ZXByaW50L3F1ZXN0L1R1dG9yaWFsL1F1ZXN0X1JldHVybkJveC1TY2FuUmV0dXJuTW92aWVfTGF0ZS5RdWVzdF9SZXR1cm5Cb3gtU2NhblJldHVybk1vdmllX0xhdGVfQwABXQAAAC9HYW1lL1ZpZGVvU3RvcmUvY29yZS9ibHVlcHJpbnQvcXVlc3QvVHV0b3JpYWwvUXVlc3RfR29Ub0JsYWNrTWFya2V0LlF1ZXN0X0dvVG9CbGFja01hcmtldF9DAAFhAAAAL0dhbWUvVmlkZW9TdG9yZS9jb3JlL2JsdWVwcmludC9xdWVzdC9UdXRvcmlhbC9RdWVzdF9FbmRUdXRvcmlhbC1CYXNpYy5RdWVzdF9FbmRUdXRvcmlhbC1CYXNpY19DAAEFAAAATm9uZQA=";
    private static readonly byte[] TutorialPatch = Convert.FromBase64String(TutorialPatchB64);

    public static string DefaultSaveDirectory()
    {
        var local = Environment.GetEnvironmentVariable("LOCALAPPDATA");
        if (string.IsNullOrWhiteSpace(local)) return string.Empty;

        var candidates = new[]
        {
            Path.Combine(local, "RetroRewind", "Saved", "SaveGames"),
            Path.Combine(local, "Retro Rewind", "Saved", "SaveGames")
        };

        foreach (var p in candidates)
            if (Directory.Exists(p)) return p;
        return candidates[0];
    }

    public static List<SaveInfo> ReadSaves(string folder)
    {
        var result = new List<SaveInfo>();
        if (!Directory.Exists(folder)) return result;

        foreach (var file in Directory.EnumerateFiles(folder, "Player_Save*.sav"))
        {
            string lower = Path.GetFileName(file).ToLowerInvariant();
            if (lower.Contains("backup") || lower.Contains("rr_skip_backup") ||
                lower.Contains("skip_tutorial_test") || lower.Contains("_test"))
                continue;

            try
            {
                byte[] data = File.ReadAllBytes(file);
                if (!IsGvas(data)) continue;

                result.Add(new SaveInfo(
                    file,
                    Path.GetFileName(file),
                    ReadStoreName(data),
                    ReadMoney(data),
                    ReadStoreLevel(data),
                    File.GetLastWriteTimeUtc(file)));
            }
            catch { }
        }

        return result.OrderByDescending(s => s.ModifiedUtc).ToList();
    }

    public static (string Status, string? BackupPath) SkipTutorial(string filePath)
    {
        byte[] data = File.ReadAllBytes(filePath);
        if (!IsGvas(data)) throw new InvalidDataException("Invalid GVAS save.");

        int q = IndexOf(data, QuestMarker);
        int st = IndexOf(data, StatisticMarker);
        if (q < 4 || st < 4 || st <= q)
            throw new InvalidDataException("Expected quest structure was not found.");

        int q0 = q - 4, st0 = st - 4;
        var current = data.AsSpan(q0, st0 - q0);

        if (IndexOf(current, Encoding.ASCII.GetBytes("QuestManager\0")) < 0 ||
            IndexOf(current, Encoding.ASCII.GetBytes("QuestDone_")) < 0)
            throw new InvalidDataException("QuestManager structure is not compatible.");

        if (IndexOf(current, EndTutorial) >= 0)
            return ("already", null);

        string backup = MakeBackup(filePath, "before_skip_tutorial");

        byte[] newData = new byte[q0 + TutorialPatch.Length + (data.Length - st0)];
        Buffer.BlockCopy(data, 0, newData, 0, q0);
        Buffer.BlockCopy(TutorialPatch, 0, newData, q0, TutorialPatch.Length);
        Buffer.BlockCopy(data, st0, newData, q0 + TutorialPatch.Length, data.Length - st0);

        if (!IsGvas(newData) || IndexOf(newData, EndTutorial) < 0)
            throw new InvalidDataException("Safety verification failed.");

        AtomicWrite(filePath, newData);
        return ("patched", backup);
    }

    public static string SetMoney(string filePath, decimal dollars)
    {
        if (dollars < 0) throw new ArgumentOutOfRangeException(nameof(dollars), "Money cannot be negative.");
        if (dollars > 9_000_000_000m) throw new ArgumentOutOfRangeException(nameof(dollars), "Amount is too high.");

        long cents = decimal.ToInt64(decimal.Round(dollars * 100m, 0, MidpointRounding.AwayFromZero));
        byte[] data = File.ReadAllBytes(filePath);
        if (!IsGvas(data)) throw new InvalidDataException("Invalid Retro Rewind save.");

        int idx = IndexOf(data, Money64Name);
        if (idx >= 0)
        {
            int pidx = IndexOf(data, Money64Prop, idx, Math.Min(data.Length, idx + 180));
            if (pidx < 0) throw new InvalidDataException("Money64 structure is not compatible.");

            byte[] marker = { 0x08, 0, 0, 0, 0 };
            int sm = IndexOf(data, marker, pidx + Money64Prop.Length,
                Math.Min(data.Length, pidx + Money64Prop.Length + 40));
            if (sm < 0) throw new InvalidDataException("Money64 value was not found.");

            int vpos = sm + marker.Length;
            if (vpos + 8 > data.Length) throw new InvalidDataException("Money64 value is incomplete.");
            BinaryPrimitives.WriteInt64LittleEndian(data.AsSpan(vpos, 8), cents);
        }
        else
        {
            int m32 = IndexOf(data, Money32Name);
            if (m32 < 0)
                throw new InvalidDataException(
                    "The money field has not been initialized yet. Buy something in-game, save, close the game and try again.");

            int ip = IndexOf(data, IntProp, m32, Math.Min(data.Length, m32 + 160));
            if (ip < 0) throw new InvalidDataException("Associated Money IntProperty was not found.");

            byte[] noneMarker = { 0x05,0,0,0,(byte)'N',(byte)'o',(byte)'n',(byte)'e',0 };
            int nonePos = IndexOf(data, noneMarker, ip, Math.Min(data.Length, ip + 120));
            if (nonePos < 0) throw new InvalidDataException("End of Money structure was not found.");

            using var ms = new MemoryStream();
            using var bw = new BinaryWriter(ms, Encoding.UTF8, leaveOpen: true);
            string money64Text = "Money64_14_4E3C8A914A3F4058F90C30BD533FEF7E";
            string propText = "Int64Property";
            bw.Write(money64Text.Length + 1);
            bw.Write(Encoding.ASCII.GetBytes(money64Text));
            bw.Write((byte)0);
            bw.Write(propText.Length + 1);
            bw.Write(Encoding.ASCII.GetBytes(propText));
            bw.Write((byte)0);
            bw.Write(new byte[4]);
            bw.Write((uint)8);
            bw.Write((byte)0);
            bw.Write(cents);
            byte[] prop = ms.ToArray();

            int moneyLenPrefix = m32 - 4;
            int sizePos = moneyLenPrefix - 9;
            if (sizePos < 0) throw new InvalidDataException("Core_Game_Struct size was not found.");

            uint oldSize = BinaryPrimitives.ReadUInt32LittleEndian(data.AsSpan(sizePos, 4));
            if (oldSize < 50 || oldSize > 10000)
                throw new InvalidDataException("Core_Game_Struct size is not compatible.");

            byte[] expanded = new byte[data.Length + prop.Length];
            Buffer.BlockCopy(data, 0, expanded, 0, nonePos);
            Buffer.BlockCopy(prop, 0, expanded, nonePos, prop.Length);
            Buffer.BlockCopy(data, nonePos, expanded, nonePos + prop.Length, data.Length - nonePos);
            BinaryPrimitives.WriteUInt32LittleEndian(expanded.AsSpan(sizePos, 4), oldSize + (uint)prop.Length);
            data = expanded;
        }

        string backup = MakeBackup(filePath, "before_money_edit");
        AtomicWrite(filePath, data);
        return backup;
    }

    public static (string BackupPath, int OldLevel) SetStoreLevel(string filePath, int newLevel)
    {
        if (newLevel < 1)
            throw new ArgumentOutOfRangeException(nameof(newLevel),
                "Level editing is only available after reaching level 1 naturally.");
        if (newLevel > 9999)
            throw new ArgumentOutOfRangeException(nameof(newLevel), "Level is too high.");

        byte[] data = File.ReadAllBytes(filePath);
        if (!IsGvas(data)) throw new InvalidDataException("Invalid Retro Rewind save.");

        int idx = IndexOf(data, LevelName);
        if (idx < 0)
            throw new InvalidDataException(
                "This save does not contain Level yet. Reach level 1 naturally, save, close the game and try again.");

        int pidx = IndexOf(data, IntProp, idx, Math.Min(data.Length, idx + 180));
        if (pidx < 0) throw new InvalidDataException("Level structure is not compatible.");

        byte[] marker = { 0x04, 0, 0, 0, 0 };
        int sm = IndexOf(data, marker, pidx + IntProp.Length,
            Math.Min(data.Length, pidx + IntProp.Length + 40));
        if (sm < 0) throw new InvalidDataException("Level value was not found.");

        int vpos = sm + marker.Length;
        int old = BinaryPrimitives.ReadInt32LittleEndian(data.AsSpan(vpos, 4));
        BinaryPrimitives.WriteInt32LittleEndian(data.AsSpan(vpos, 4), newLevel);

        string backup = MakeBackup(filePath, "before_level_edit");
        AtomicWrite(filePath, data);
        return (backup, old);
    }

    private static decimal? ReadMoney(byte[] data)
    {
        int idx = IndexOf(data, Money64Name);
        if (idx >= 0)
        {
            int pidx = IndexOf(data, Money64Prop, idx, Math.Min(data.Length, idx + 180));
            if (pidx < 0) return null;
            byte[] marker = { 0x08, 0, 0, 0, 0 };
            int sm = IndexOf(data, marker, pidx + Money64Prop.Length,
                Math.Min(data.Length, pidx + Money64Prop.Length + 40));
            if (sm < 0) return null;
            int vpos = sm + marker.Length;
            if (vpos + 8 > data.Length) return null;
            return BinaryPrimitives.ReadInt64LittleEndian(data.AsSpan(vpos, 8)) / 100m;
        }
        return 550m;
    }

    private static int? ReadStoreLevel(byte[] data)
    {
        int idx = IndexOf(data, LevelName);
        if (idx < 0) return null;
        int pidx = IndexOf(data, IntProp, idx, Math.Min(data.Length, idx + 180));
        if (pidx < 0) return null;
        byte[] marker = { 0x04, 0, 0, 0, 0 };
        int sm = IndexOf(data, marker, pidx + IntProp.Length,
            Math.Min(data.Length, pidx + IntProp.Length + 40));
        if (sm < 0) return null;
        int vpos = sm + marker.Length;
        return vpos + 4 <= data.Length
            ? BinaryPrimitives.ReadInt32LittleEndian(data.AsSpan(vpos, 4))
            : null;
    }

    private static string? ReadStoreName(byte[] data)
    {
        string ascii = Encoding.ASCII.GetString(data);
        var match = Regex.Match(ascii, @"Name_18_[0-9A-F]+\x00");
        if (!match.Success) return null;

        int start = match.Index + match.Length;
        int end = Math.Min(data.Length, start + 260);
        var chunk = data.AsSpan(start, end - start);
        int tp = IndexOf(chunk, TextProperty);
        if (tp < 0) return null;

        var region = chunk[(tp + TextProperty.Length)..];
        for (int i = 0; i <= region.Length - 5; i++)
        {
            int n = BinaryPrimitives.ReadInt32LittleEndian(region.Slice(i, 4));
            if (n < 2 || n > 80 || i + 4 + n > region.Length) continue;
            var raw = region.Slice(i + 4, n);
            if (raw[^1] != 0) continue;
            try
            {
                string s = new UTF8Encoding(false, true).GetString(raw[..^1]);
                if (string.IsNullOrEmpty(s) || s.Any(c => c < 32) ||
                    s == "TextProperty" || Regex.IsMatch(s, @"^[0-9A-F]{20,}$"))
                    continue;
                return s;
            }
            catch { }
        }
        return null;
    }

    private static string MakeBackup(string filePath, string tag)
    {
        var fi = new FileInfo(filePath);
        string dir = Path.Combine(fi.DirectoryName!, "RetroRewindTool_Backups");
        Directory.CreateDirectory(dir);
        string stamp = DateTime.Now.ToString("yyyyMMdd_HHmmss");
        string backup = Path.Combine(dir, $"{Path.GetFileNameWithoutExtension(fi.Name)}_{tag}_{stamp}{fi.Extension}");
        File.Copy(filePath, backup, false);
        return backup;
    }

    private static void AtomicWrite(string filePath, byte[] data)
    {
        string dir = Path.GetDirectoryName(filePath)!;
        string tmp = Path.Combine(dir, $"{Path.GetFileNameWithoutExtension(filePath)}_{Guid.NewGuid():N}.tmp");
        try
        {
            File.WriteAllBytes(tmp, data);
            File.Move(tmp, filePath, true);
        }
        finally
        {
            if (File.Exists(tmp)) File.Delete(tmp);
        }
    }

    private static bool IsGvas(byte[] data) =>
        data.Length >= 4 && data[0] == 'G' && data[1] == 'V' && data[2] == 'A' && data[3] == 'S';

    private static int IndexOf(byte[] h, byte[] n) => IndexOf(h, n, 0, h.Length);

    private static int IndexOf(byte[] h, byte[] n, int start, int end)
    {
        if (n.Length == 0 || start < 0 || end > h.Length || start >= end) return -1;
        int x = IndexOf(h.AsSpan(start, end - start), n);
        return x < 0 ? -1 : start + x;
    }

    private static int IndexOf(ReadOnlySpan<byte> h, ReadOnlySpan<byte> n)
    {
        if (n.Length == 0 || n.Length > h.Length) return -1;
        for (int i = 0; i <= h.Length - n.Length; i++)
            if (h.Slice(i, n.Length).SequenceEqual(n)) return i;
        return -1;
    }
}
