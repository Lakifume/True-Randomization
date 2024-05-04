using System.Collections.Generic;
using UAssetAPI.PropertyTypes.Objects;
using UAssetAPI.UnrealTypes;

namespace UAssetSnippet;

public class DetachedObjectPropertyData : PropertyData<int>
{
    private static readonly FString _currentPropertyType = new("DetachedObjectProperty");

    public List<int> UsedExports = default;
    public override FString PropertyType => _currentPropertyType;
    public DetachedObjectPropertyData(FName name, List<int> usedExports) : this(name)
    {
        UsedExports = usedExports;
    }

    public DetachedObjectPropertyData(FName name) : base(name) { }

    public DetachedObjectPropertyData() { }
}