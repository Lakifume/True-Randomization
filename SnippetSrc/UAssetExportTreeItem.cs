using System.Collections.Generic;

namespace UAssetSnippet;

public class UAssetExportTreeItem
{
    public int ExportIndex = -1; // 0 - indexed!
    public bool IsRoot = true;
    public List<UAssetExportTreeItem> AttachedChildren = [];
}