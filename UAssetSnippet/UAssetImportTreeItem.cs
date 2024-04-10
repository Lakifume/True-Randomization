using System.Collections.Generic;

namespace UAssetSnippet;

public class UAssetImportTreeItem
{
    public int ImportIndex = -1; // 0 - indexed!
    public bool IsRoot = true;
    public List<int> ParentImports = [];
}
