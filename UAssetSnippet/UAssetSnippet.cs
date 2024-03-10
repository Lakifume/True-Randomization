using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Formatters.Binary;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using UAssetAPI;
using UAssetAPI.PropertyTypes;
using UAssetAPI.UnrealTypes;
using UAssetAPI.PropertyTypes.Objects;
using UAssetAPI.PropertyTypes.Structs;

namespace UAssetSnippet
{
    public class UAssetSnippet
    {
        private int PERSISTENT_LEVEL_EXPORT_IDENTIFIER = -6969420;

        public class UAssetExportTreeItem
        {
            public int ExportIndex = -1; // 0 - indexed!
            public bool IsRoot = true;
            public List<UAssetExportTreeItem> AttachedChildren = new List<UAssetExportTreeItem>();
        }
        public class UAssetImportTreeItem
        {
            public int ImportIndex = -1; // 0 - indexed!
            public bool IsRoot = true;
            public List<int> ParentImports = new List<int>();
        }
        public class DetachedObjectPropertyData : PropertyData<int>
        {
            public List<int> UsedExports = default(List<int>);
            private static readonly FString CurrentPropertyType = new FString("DetachedObjectProperty");
            public override FString PropertyType { get { return CurrentPropertyType; } }
            public DetachedObjectPropertyData(FName name, List<int> usedExports) : base(name)
            {
                UsedExports = usedExports;
            }
            public DetachedObjectPropertyData() { }
        }

        public class AttachToAssetInfo
        {
            public List<int> AttachedExportMap = new List<int>();
        }

        public UAsset StrippedUasset;
        public List<int> UsedImports = new List<int>();
        public HashSet<int> UsedImportSet = new HashSet<int>();
        public List<int> UsedExports = new List<int>();
        public HashSet<int> UsedExportSet = new HashSet<int>();
        public int RootExportIndex = -1; // 0 based list index! NOT the 1 based export number.
        public List<UAssetExportTreeItem> ExportTree = new List<UAssetExportTreeItem>();
        public List<UAssetImportTreeItem> ImportTree = new List<UAssetImportTreeItem>();

        public UAssetSnippet(UAsset originalUAsset, int rootExportIndex)
        {
            RootExportIndex = rootExportIndex;

            BuildImportTree(originalUAsset);
            BuildExportTree(originalUAsset);
            BuildUsedExports(originalUAsset);
            BuildUsedImports(originalUAsset);
            CreateStrippedUAsset(originalUAsset);
        }

        private void BuildImportTree(UAsset originalUAsset)
        {
            // Build dependency tree
            int importIndex = 0;
            foreach (Import import in originalUAsset.Imports)
            {
                // Set up class for dependency tree
                UAssetImportTreeItem importTreeItem = new UAssetImportTreeItem();
                importTreeItem.ImportIndex = importIndex;
                ImportTree.Add(
                    importTreeItem
                );
                importIndex++;
            }

            // Populate tree based on imports that reference via outerIndex
            importIndex = 0;
            foreach (Import import in originalUAsset.Imports)
            {
                UAssetImportTreeItem importTreeItem = ImportTree[importIndex];
                if (import.OuterIndex.Index < 0)
                {
                    int parentImportIndex = import.OuterIndex.Index;
                    while (parentImportIndex != 0)
                    {
                        int arrayParentIndex = Math.Abs(parentImportIndex) - 1;
                        if (arrayParentIndex >= 0 && arrayParentIndex < ImportTree.Count)
                        {
                            importTreeItem.ParentImports.Add(arrayParentIndex);
                            parentImportIndex = originalUAsset.Imports[arrayParentIndex].OuterIndex.Index;
                        }
                        else
                        {
                            break;
                        }
                    }
                }
                importIndex++;
            }
        }

        private void BuildExportTree(UAsset originalUAsset)
        {
            // Build dependency tree
            int exportIndex = 0;
            foreach (Export baseExport in originalUAsset.Exports)
            {
                // Set up class for dependency tree
                UAssetExportTreeItem exportTreeItem = new UAssetExportTreeItem();
                exportTreeItem.ExportIndex = exportIndex;
                ExportTree.Add(
                    exportTreeItem
                );
                exportIndex++;
            }

            // Populate attach parent for each exportTree item
            exportIndex = 0;
            foreach (Export baseExport in originalUAsset.Exports)
            {
                if (baseExport is NormalExport export)
                {
                    foreach (PropertyData propertyData in export.Data)
                    {
                        string propertyName = propertyData.Name.Value.ToString();
                        if (propertyData is ObjectPropertyData objectPropertyData)
                        {
                            if (propertyName == "AttachParent")
                            {
                                try
                                {
                                    ExportTree[exportIndex].IsRoot = false;
                                    ExportTree[objectPropertyData.Value.Index - 1].AttachedChildren.Add(ExportTree[exportIndex]);
                                }
                                catch (Exception e)
                                {
                                    Console.Write("Set up Attach Parent error ", e);
                                }
                            }
                        }
                    }
                }
                exportIndex++;
            }
        }

        private void BuildUsedExports(UAsset originalUAsset)
        {
            UsedExports.Add(RootExportIndex);
            UsedExportSet.Add(RootExportIndex);
            for (int i = 0; i < UsedExports.Count; i++)
            {
                Export checkExport = originalUAsset.Exports[UsedExports[i]];
                if (checkExport is NormalExport normalCheckExport)
                {
                    List<int> referencedObjects = GetPropertyDataReferencedObjects(new List<PropertyData>(normalCheckExport.Data));
                    foreach (int referencedObjectIndex in referencedObjects)
                    {
                        if (referencedObjectIndex >= 0 && referencedObjectIndex < ExportTree.Count)
                        {
                            if (!UsedExportSet.Contains(referencedObjectIndex))
                            {
                                UsedExportSet.Add(referencedObjectIndex);
                                UsedExports.Add(referencedObjectIndex);
                                List<int> attachedChildrenReferencedObjects = GetAttachedChildrenReferencedObjects(ExportTree[referencedObjectIndex]);
                                foreach (int attachedReferencedObjectIndex in attachedChildrenReferencedObjects)
                                {
                                    if (!UsedExportSet.Contains(attachedReferencedObjectIndex))
                                    {
                                        UsedExportSet.Add(attachedReferencedObjectIndex);
                                        UsedExports.Add(attachedReferencedObjectIndex);
                                    }
                                }
                            }
                        }
                        else
                        {
                            // Object referenced undefined index, ignore
                        }
                    }
                }
            }
        }

        private void BuildUsedImports(UAsset originalUAsset)
        {
            for (int i = 0; i < UsedExports.Count; i++)
            {
                Export usedExport = originalUAsset.Exports[UsedExports[i]];
                if (usedExport.ClassIndex.Index < 0)
                {
                    int arrayClassIndex = Math.Abs(usedExport.ClassIndex.Index) - 1;
                    if (!UsedImportSet.Contains(arrayClassIndex))
                    {
                        UsedImportSet.Add(arrayClassIndex);
                        UsedImports.Add(arrayClassIndex);
                    }
                }
                if (usedExport.TemplateIndex.Index < 0)
                {
                    int arrayTemplateIndex = Math.Abs(usedExport.TemplateIndex.Index) - 1;
                    if (!UsedImportSet.Contains(arrayTemplateIndex))
                    {
                        UsedImportSet.Add(arrayTemplateIndex);
                        UsedImports.Add(arrayTemplateIndex);
                    }
                }
                List<List<FPackageIndex>> dependencyMappingArrays = new List<List<FPackageIndex>>(){
                usedExport.SerializationBeforeSerializationDependencies,
                usedExport.CreateBeforeSerializationDependencies,
                usedExport.SerializationBeforeCreateDependencies,
                usedExport.CreateBeforeCreateDependencies
            };
                foreach (List<FPackageIndex> dependencyMap in dependencyMappingArrays)
                {
                    foreach (FPackageIndex packageIndex in dependencyMap)
                    {
                        if (packageIndex.Index < 0)
                        {
                            int arrayDepIndex = Math.Abs(packageIndex.Index) - 1;
                            if (!UsedImportSet.Contains(arrayDepIndex))
                            {
                                UsedImportSet.Add(arrayDepIndex);
                                UsedImports.Add(arrayDepIndex);
                            }
                        }
                    }
                }
                if (usedExport is NormalExport normalExport)
                {
                    BuildUsedImportsFromPropertyData(normalExport.Data);
                }
            }
            List<int> foundParentImports = UsedImports.ToList();
            while (foundParentImports.Count > 0)
            {
                List<int> newFoundParentImports = new List<int>();
                foreach (int importIndex in foundParentImports)
                {
                    Import usedImport = originalUAsset.Imports[importIndex];
                    if (usedImport.OuterIndex.Index < 0)
                    {
                        int arrayOuterIndex = Math.Abs(usedImport.OuterIndex.Index) - 1;
                        if (!UsedImportSet.Contains(arrayOuterIndex))
                        {
                            UsedImportSet.Add(arrayOuterIndex);
                            UsedImports.Add(arrayOuterIndex);
                            newFoundParentImports.Add(arrayOuterIndex);
                        }
                    }
                }
                foundParentImports = newFoundParentImports;
            }
            UsedImports.Reverse();
        }

        private void BuildUsedImportsFromPropertyData(List<PropertyData> propertyDataList)
        {
            foreach (PropertyData propertyData in propertyDataList)
            {
                if (propertyData is ObjectPropertyData objectPropertyData)
                {
                    if (objectPropertyData.IsImport())
                    {
                        int arrayDepIndex = Math.Abs(objectPropertyData.Value.Index) - 1;
                        if (!UsedImportSet.Contains(arrayDepIndex))
                        {
                            UsedImportSet.Add(arrayDepIndex);
                            UsedImports.Add(arrayDepIndex);
                        }
                    }
                }
                else if (propertyData is ArrayPropertyData arrayPropertyData)
                {
                    BuildUsedImportsFromPropertyData(arrayPropertyData.Value.ToList<PropertyData>());
                }
                else if (propertyData is StructPropertyData structPropertyData)
                {
                    BuildUsedImportsFromPropertyData(structPropertyData.Value);
                }
            }
        }

        private void CreateStrippedUAsset(UAsset originalUAsset)
        {
            UAsset strippedUAsset = new UAsset(originalUAsset.EngineVersion);
            strippedUAsset.Imports = new List<Import>();
            strippedUAsset.Exports = new List<Export>();
            strippedUAsset.Generations = new List<FGenerationInfo>();
            strippedUAsset.ChunkIDs = new int[0];
            strippedUAsset.SoftPackageReferenceList = new List<FString>();
            strippedUAsset.AssetRegistryData = new List<int>();
            strippedUAsset.CustomVersionContainer = new List<CustomVersion>();
            strippedUAsset.ClearNameIndexList();
            int importStartIndex = strippedUAsset.Imports.Count;
            int exportStartIndex = strippedUAsset.Exports.Count;

            // Add new imports to end of current asset's imports
            List<int> mappedImports = new List<int>();
            List<int> newlyAddedImports = new List<int>();
            foreach (int originalImportIndex in UsedImports)
            {
                Import originalImport = originalUAsset.Imports[originalImportIndex];
                newlyAddedImports.Add(originalImportIndex);
                mappedImports.Add(strippedUAsset.Imports.Count);
                Import clonedImport = CloneImport(originalImport, strippedUAsset);

                if (clonedImport.OuterIndex.Index < 0)
                {
                    int importOuterIndex = clonedImport.OuterIndex.Index;
                    int importOuterArrayIndex = Math.Abs(importOuterIndex) - 1;
                    int newImportOuterIndex = -(UsedImports.IndexOf(importOuterArrayIndex) + 1);
                    clonedImport.OuterIndex = FPackageIndex.FromRawIndex(newImportOuterIndex);
                }

                strippedUAsset.Imports.Add(clonedImport);
            }

            // Find level export index
            int originalPersistentLevelExportNumber = 0;
            foreach (Export export in originalUAsset.Exports)
            {
                originalPersistentLevelExportNumber++;
                if (export is LevelExport levelExport)
                {
                    break;
                }
            }

            // Cloned used exports and add to end of current asset's exports
            bool isPrimaryExport = true;
            foreach (int originalExportIndex in UsedExports)
            {
                //Console.Write("Cloning export " + originalExportIndex);
                Export clonedExport = CloneExport(originalUAsset, originalUAsset.Exports[originalExportIndex], strippedUAsset, exportStartIndex, mappedImports);
                if (isPrimaryExport)
                {
                    clonedExport.bIsAsset = true;
                    clonedExport.OuterIndex.Index = 0;
                }
                if (clonedExport.OuterIndex.Index == originalPersistentLevelExportNumber)
                {
                    clonedExport.OuterIndex.Index = PERSISTENT_LEVEL_EXPORT_IDENTIFIER;
                }
                try
                {
                    int oldClassIndex = originalUAsset.Exports[originalExportIndex].ClassIndex.Index;
                    int oldClassIndexArrayIndex = Math.Abs(oldClassIndex) - 1;
                    if (oldClassIndexArrayIndex >= 0)
                    {
                        clonedExport.ClassIndex = new FPackageIndex(-(mappedImports[UsedImports.IndexOf(oldClassIndexArrayIndex)] + 1));
                    }
                    int oldTemplateIndex = originalUAsset.Exports[originalExportIndex].TemplateIndex.Index;
                    int oldTemplateIndexArrayIndex = Math.Abs(oldTemplateIndex) - 1;
                    if (oldTemplateIndexArrayIndex >= 0)
                    {
                        clonedExport.TemplateIndex = new FPackageIndex(-(mappedImports[UsedImports.IndexOf(oldTemplateIndexArrayIndex)] + 1));
                    }
                    List<List<FPackageIndex>> dependencyMappingArrays = new List<List<FPackageIndex>>(){
                    clonedExport.SerializationBeforeSerializationDependencies,
                    clonedExport.CreateBeforeSerializationDependencies,
                    clonedExport.SerializationBeforeCreateDependencies,
                    clonedExport.CreateBeforeCreateDependencies
                };
                    FPackageIndex defaultIndex = FPackageIndex.FromRawIndex(0);
                    for (int j = 0; j < dependencyMappingArrays.Count; j++)
                    {
                        List<FPackageIndex> dependencyArray = new List<FPackageIndex>(dependencyMappingArrays[j]);
                        List<FPackageIndex> newDependencyArray = dependencyMappingArrays[j];
                        newDependencyArray.Clear();
                        HashSet<int> usedDeps = new HashSet<int>();
                        for (int i = 0; i < dependencyArray.Count; i++)
                        {
                            FPackageIndex index = dependencyArray[i];
                            FPackageIndex newIndex = defaultIndex;
                            if (index.Index < 0)
                            {
                                int arrayIndex = Math.Abs(index.Index) - 1;
                                if (arrayIndex >= 0)
                                {
                                    int usedImportIndex = UsedImports.IndexOf(arrayIndex);
                                    if (usedImportIndex > -1)
                                    {
                                        newIndex = FPackageIndex.FromRawIndex(-(mappedImports[usedImportIndex] + 1));
                                    }
                                    else
                                    {
                                        Console.Write("While handling export ", originalExportIndex);
                                        Console.Write("Could not map import index ", index.Index);
                                    }
                                }
                            }
                            else if (index.Index > 0)
                            {
                                int newExportIndex = index.Index - 1;
                                if (index.Index == originalPersistentLevelExportNumber)
                                {
                                    newExportIndex = PERSISTENT_LEVEL_EXPORT_IDENTIFIER;
                                }
                                else
                                {
                                    if (UsedExports != null)
                                    {
                                        newExportIndex = UsedExports.IndexOf(index.Index - 1);
                                    }
                                    if (newExportIndex != -1)
                                    {
                                        newExportIndex += exportStartIndex + 1;
                                    }
                                    else
                                    {
                                        newExportIndex = index.Index;
                                    }
                                }
                                newIndex = FPackageIndex.FromRawIndex(newExportIndex);
                            }
                            if (!usedDeps.Contains(newIndex.Index))
                            {
                                usedDeps.Add(newIndex.Index);
                                newDependencyArray.Add(newIndex);
                            }
                        }
                        dependencyMappingArrays[j] = newDependencyArray;
                    }
                }
                catch (Exception e)
                {
                    Console.Write(e);
                }
                strippedUAsset.Exports.Add(clonedExport);
                isPrimaryExport = false;
            }

            StrippedUasset = strippedUAsset;
            UsedExports = null;
            UsedImports = null;
        }

        private List<int> GetAttachedChildrenReferencedObjects(UAssetExportTreeItem exportRoot)
        {
            List<int> referencedObjects = new List<int>();
            foreach (UAssetExportTreeItem exportChild in exportRoot.AttachedChildren)
            {
                referencedObjects.Add(exportChild.ExportIndex);
                referencedObjects = referencedObjects.Concat(GetAttachedChildrenReferencedObjects(exportChild)).ToList();
            }
            return referencedObjects;
        }

        private List<int> GetPropertyDataReferencedObjects(List<PropertyData> propertyDataList)
        {
            List<int> referencedObjects = new List<int>();
            foreach (PropertyData propertyData in propertyDataList)
            {
                if (propertyData is ObjectPropertyData objectPropertyData)
                {
                    referencedObjects.Add(objectPropertyData.Value.Index - 1);
                }
                else if (propertyData is ArrayPropertyData arrayPropertyData)
                {
                    referencedObjects = referencedObjects.Concat(GetPropertyDataReferencedObjects(arrayPropertyData.Value.ToList<PropertyData>())).ToList();
                }
            }
            return referencedObjects;
        }

        public AttachToAssetInfo AddToUAsset(UAsset attachToAsset, string exportObjectName = "TEST_ADD_SNIPPET")
        {
            AttachToAssetInfo attachInfo = new AttachToAssetInfo();

            int importStartIndex = attachToAsset.Imports.Count;
            int exportStartIndex = attachToAsset.Exports.Count;

            // Add new imports to end of current asset's imports
            List<int> mappedImports = new List<int>();
            List<int> newlyAddedImports = new List<int>();
            int snippetImportIndex = 0;
            foreach (Import snippetImport in StrippedUasset.Imports)
            {
                int newImportIndex = GetExistingImportIndex(snippetImport, attachToAsset);
                if (newImportIndex > -1)
                {
                    mappedImports.Add(newImportIndex);
                }
                else
                {
                    newlyAddedImports.Add(snippetImportIndex);
                    mappedImports.Add(attachToAsset.Imports.Count);
                    Import clonedImport = CloneImport(snippetImport, attachToAsset);
                    attachToAsset.Imports.Add(clonedImport);
                }
                snippetImportIndex++;
            }

            // Modify outer index for each import (this equates to a noop if the import already exists in the file)
            for (int i = 0; i < StrippedUasset.Imports.Count; i++)
            {
                if (newlyAddedImports.IndexOf(i) > -1)
                {
                    int mappedImportIndex = mappedImports[i];
                    try
                    {
                        int arrayOuterIndex = Math.Abs(attachToAsset.Imports[mappedImportIndex].OuterIndex.Index) - 1;
                        // Reassign outerIndex if it's not 0 (top level package)
                        if (arrayOuterIndex != -1)
                        {
                            attachToAsset.Imports[mappedImportIndex].OuterIndex.Index = -(mappedImports[arrayOuterIndex] + 1);
                        }
                    }
                    catch (Exception e)
                    {
                        Console.Write(e);
                    }
                }
            }

            // Find level export index
            int persistentLevelExportNumber = 0;
            List<FName> levelExportNames = new List<FName>();
            foreach (Export export in attachToAsset.Exports)
            {
                persistentLevelExportNumber++;
                if (export is LevelExport levelExport)
                {
                    foreach (int exportIndex in levelExport.IndexData)
                    {
                        if (exportIndex > 0 && exportIndex <= attachToAsset.Exports.Count)
                        {
                            levelExportNames.Add(attachToAsset.Exports[exportIndex - 1].ObjectName);
                        }
                    }
                    break;
                }
            }
            List<int> levelExportExtraIndexData = new List<int>();

            // Cloned used exports and add to end of current asset's exports
            int currentAdditionalExportIndex = 0;
            foreach (Export snippetExport in StrippedUasset.Exports)
            {
                bool isPersistentLevelParentExport = snippetExport.OuterIndex.Index == PERSISTENT_LEVEL_EXPORT_IDENTIFIER;
                Export clonedExport = CloneExport(StrippedUasset, snippetExport, attachToAsset, exportStartIndex, mappedImports);
                if (isPersistentLevelParentExport)
                {
                    clonedExport.OuterIndex = FPackageIndex.FromRawIndex(persistentLevelExportNumber);
                    levelExportExtraIndexData.Add(attachToAsset.Exports.Count);
                }
                try
                {
                    clonedExport.bIsAsset = false;
                    int oldClassIndex = clonedExport.ClassIndex.Index;
                    int oldClassIndexArrayIndex = Math.Abs(oldClassIndex) - 1;
                    if (oldClassIndexArrayIndex >= 0)
                    {
                        clonedExport.ClassIndex = new FPackageIndex(-(mappedImports[oldClassIndexArrayIndex] + 1));
                    }
                    int oldTemplateIndex = clonedExport.TemplateIndex.Index;
                    int oldTemplateIndexArrayIndex = Math.Abs(oldTemplateIndex) - 1;
                    if (oldTemplateIndexArrayIndex >= 0)
                    {
                        clonedExport.TemplateIndex = new FPackageIndex(-(mappedImports[oldTemplateIndexArrayIndex] + 1));
                    }

                    List<List<FPackageIndex>> dependencyMappingArrays = new List<List<FPackageIndex>>(){
                    clonedExport.SerializationBeforeSerializationDependencies,
                    clonedExport.CreateBeforeSerializationDependencies,
                    clonedExport.SerializationBeforeCreateDependencies,
                    clonedExport.CreateBeforeCreateDependencies
                };
                    FPackageIndex defaultIndex = FPackageIndex.FromRawIndex(0);
                    for (int j = 0; j < dependencyMappingArrays.Count; j++)
                    {
                        List<FPackageIndex> dependencyArray = new List<FPackageIndex>(dependencyMappingArrays[j]);
                        List<FPackageIndex> newDependencyArray = dependencyMappingArrays[j];
                        newDependencyArray.Clear();
                        HashSet<int> usedDeps = new HashSet<int>();
                        for (int i = 0; i < dependencyArray.Count; i++)
                        {
                            FPackageIndex index = dependencyArray[i];
                            FPackageIndex newIndex = defaultIndex;
                            if (index.Index == PERSISTENT_LEVEL_EXPORT_IDENTIFIER)
                            {
                                newIndex = FPackageIndex.FromRawIndex(persistentLevelExportNumber);
                            }
                            else if (index.Index < 0)
                            {
                                int arrayIndex = Math.Abs(index.Index) - 1;
                                if (arrayIndex >= 0)
                                {
                                    newIndex = FPackageIndex.FromRawIndex(-(mappedImports[arrayIndex] + 1));
                                }
                            }
                            else if (index.Index > 0)
                            {
                                int newExportIndex = index.Index - 1;
                                if (newExportIndex != -1)
                                {
                                    newExportIndex += exportStartIndex + 1;
                                }
                                else
                                {
                                    newExportIndex = index.Index;
                                }
                                newIndex = FPackageIndex.FromRawIndex(newExportIndex);
                            }
                            if (!usedDeps.Contains(newIndex.Index))
                            {
                                usedDeps.Add(newIndex.Index);
                                newDependencyArray.Add(newIndex);
                            }
                        }
                        dependencyMappingArrays[j] = newDependencyArray;
                    }
                }
                catch (Exception e)
                {
                    Console.Write(e);
                }
                attachToAsset.Exports.Add(clonedExport);
            }

            // Rename base export
            try
            {
                attachToAsset.Exports[exportStartIndex].ObjectName = FName.FromString(attachToAsset, exportObjectName);
            }
            catch (Exception e)
            {
                Console.Write(e);
            }

            // Add the base export (blueprint) to the level
            int levelExportNumber = 1;
            foreach (Export baseExport in attachToAsset.Exports)
            {
                if (baseExport is LevelExport levelExport)
                {
                    levelExportExtraIndexData.Add(exportStartIndex);
                    foreach (int levelExportExtraIndex in levelExportExtraIndexData)
                    {
                        int newExportNumber = levelExportExtraIndex + 1;
                        levelExport.IndexData.Add(newExportNumber);
                        attachToAsset.Exports[levelExportExtraIndex].OuterIndex.Index = levelExportNumber;
                        attachToAsset.Exports[levelExportExtraIndex].CreateBeforeCreateDependencies[0] = FPackageIndex.FromRawIndex(levelExportNumber);
                        levelExport.CreateBeforeSerializationDependencies.Add(FPackageIndex.FromRawIndex(newExportNumber));

                        Export addedLevelExport = attachToAsset.Exports[newExportNumber - 1];
                        FName newObjectName = GuaranteeUniqueFNameFromList(addedLevelExport.ObjectName, levelExportNames, attachToAsset);
                        levelExportNames.Add(newObjectName);
                        addedLevelExport.ObjectName = newObjectName;
                    }
                    break;
                }
                levelExportNumber++;
            }

            return attachInfo;
        }

        public bool IsFNameInList(FName fName, List<FName> list)
        {
            bool isInList = false;
            foreach (FName checkFName in list)
            {
                if (fName.Equals(checkFName))
                {
                    isInList = true;
                    break;
                }
            }
            return isInList;
        }

        public FName GuaranteeUniqueFNameFromList(FName fName, List<FName> list, UAsset attachToAsset)
        {
            int number = fName.Number;
            FName newFName = new FName(attachToAsset, fName.Value, number);
            while (IsFNameInList(newFName, list))
            {
                number++;
                newFName.Number = number;
            }
            return newFName;
        }

        public bool IsCloneableImport(string classPackage, string className)
        {
            if (className.EndsWith("Component") || classPackage == "/Script/ProjectBlood" || classPackage == "/Script/Engine")
            {
                return false;
            }
            return true;
        }
        public int GetExistingImportIndex(Import checkImport, UAsset uAsset)
        {
            return -1;
            // int importIndex = -1;
            // string classPackageString = checkImport.ClassPackage.ToString();
            // string classNameString = checkImport.ClassName.ToString();
            // string objectNameString = checkImport.ObjectName.ToString();

            // if (!IsCloneableImport(classPackageString, classNameString)) {
            //     return importIndex;
            // }

            // for (int i = 0; i < uAsset.Imports.Count; i++) {
            //     Import import = uAsset.Imports[i];
            //     if (import.ObjectName.ToString() == objectNameString && import.ClassName.ToString() == classNameString && import.ClassPackage.ToString() == classPackageString) {
            //         importIndex = i;
            //         break;
            //     }
            // }
            // return importIndex;
        }

        public Import CloneImport(Import originalImport, UAsset attachToAsset)
        {
            // attachToAsset.AddNameReference(originalImport.ClassPackage.Value);
            // attachToAsset.AddNameReference(originalImport.ClassName.Value);
            // attachToAsset.AddNameReference(originalImport.ObjectName.Value);
            // FName classPackage = new FName(attachToAsset, originalImport.ClassPackage.Value, originalImport.ClassPackage.Number);
            // FName className = new FName(attachToAsset, originalImport.ClassName.Value, originalImport.ClassName.Number);
            // FName objectName = new FName(attachToAsset, originalImport.ObjectName.Value, originalImport.ObjectName.Number);
            Import clonedImport = new Import(
                FName.FromString(attachToAsset, originalImport.ClassPackage.Value.Value),
                FName.FromString(attachToAsset, originalImport.ClassName.Value.Value),
                FPackageIndex.FromRawIndex(originalImport.OuterIndex.Index),
                FName.FromString(attachToAsset, originalImport.ObjectName.ToString()) // .Value.Value?
            );
            return clonedImport;
        }

        public Export CloneExport(UAsset originalUAsset, Export export, UAsset attachToAsset, int exportStartIndex, List<int> mappedImports)
        {
            int newOuterIndex = export.OuterIndex.Index - 1;
            if (UsedExports != null)
            {
                newOuterIndex = UsedExports.IndexOf(export.OuterIndex.Index - 1);
            }
            if (newOuterIndex != -1)
            {
                newOuterIndex += exportStartIndex + 1;
            }
            else
            {
                newOuterIndex = export.OuterIndex.Index;
            }
            byte[] extras = new byte[export.Extras.Length];
            export.Extras.CopyTo(extras, 0);
            Export newExport = new Export(
                attachToAsset,
                extras
            );
            Export newTypedExport = newExport;
            if (export is ClassExport classExport)
            {
                newTypedExport = new ClassExport(newExport);
            }
            else if (export is NormalExport normalExport)
            {
                newTypedExport = new NormalExport(newExport);
                ((NormalExport)newTypedExport).Data = ClonePropertyData(originalUAsset, new List<PropertyData>(normalExport.Data), attachToAsset, exportStartIndex, mappedImports);
            }
            newTypedExport.ClassIndex = FPackageIndex.FromRawIndex(export.ClassIndex.Index);
            newTypedExport.SuperIndex = FPackageIndex.FromRawIndex(export.SuperIndex.Index);
            newTypedExport.TemplateIndex = FPackageIndex.FromRawIndex(export.TemplateIndex.Index);
            newTypedExport.OuterIndex = FPackageIndex.FromRawIndex(newOuterIndex);
            newTypedExport.ObjectName = FName.FromString(attachToAsset, export.ObjectName.ToString());
            newTypedExport.ObjectFlags = export.ObjectFlags;
            newTypedExport.SerialSize = Convert.ToInt32(export.SerialSize);
            newTypedExport.SerialOffset = Convert.ToInt32(export.SerialOffset);
            newTypedExport.bForcedExport = export.bForcedExport;
            newTypedExport.bNotForClient = export.bNotForClient;
            newTypedExport.bNotForServer = export.bNotForServer;
            newTypedExport.PackageGuid = export.PackageGuid;
            newTypedExport.PackageFlags = export.PackageFlags;
            newTypedExport.bNotAlwaysLoadedForEditorGame = export.bNotAlwaysLoadedForEditorGame;
            newTypedExport.bIsAsset = export.bIsAsset;
            newTypedExport.SerializationBeforeSerializationDependencies = new List<FPackageIndex>(export.SerializationBeforeSerializationDependencies);
            newTypedExport.CreateBeforeSerializationDependencies = new List<FPackageIndex>(export.CreateBeforeSerializationDependencies);
            newTypedExport.SerializationBeforeCreateDependencies = new List<FPackageIndex>(export.SerializationBeforeCreateDependencies);
            newTypedExport.CreateBeforeCreateDependencies = new List<FPackageIndex>(export.CreateBeforeCreateDependencies);

            return newTypedExport;
        }

        public System.Object DeepClone(System.Object original)
        {
            MemoryStream stream = new MemoryStream();
            BinaryFormatter formatter = new BinaryFormatter();
            formatter.Context = new StreamingContext(StreamingContextStates.Clone);
            formatter.Serialize(stream, original);
            stream.Position = 0;
            return (formatter.Deserialize(stream));
        }

        public List<PropertyData> ClonePropertyData(UAsset originalUAsset, List<PropertyData> propertyDataList, UAsset attachToAsset, int exportStartIndex, List<int> mappedImports)
        {
            List<PropertyData> newPropertyDataList = new List<PropertyData>();
            foreach (PropertyData propertyData in propertyDataList)
            {
                FName newPropertyName = FName.FromString(attachToAsset, propertyData.Name.Value.Value);
                attachToAsset.AddNameReference(newPropertyName.Value);
                attachToAsset.AddNameReference(propertyData.PropertyType);
                if (propertyData is ArrayPropertyData arrayPropertyData)
                {
                    ArrayPropertyData newArrayPropertyData = new ArrayPropertyData(newPropertyName);
                    newArrayPropertyData.Value = ClonePropertyData(originalUAsset, arrayPropertyData.Value.ToList<PropertyData>(), attachToAsset, exportStartIndex, mappedImports).ToArray();
                    newPropertyDataList.Add(newArrayPropertyData);
                }
                else if (propertyData is BoolPropertyData boolPropertyData)
                {
                    BoolPropertyData newBoolPropertyData = new BoolPropertyData(newPropertyName);
                    newBoolPropertyData.Value = boolPropertyData.Value;
                    newPropertyDataList.Add(newBoolPropertyData);
                }
                else if (propertyData is BytePropertyData bytePropertyData)
                {
                    BytePropertyData newBytePropertyData = new BytePropertyData(newPropertyName);
                    newBytePropertyData.ByteType = bytePropertyData.ByteType;
                    if (newBytePropertyData.ByteType == BytePropertyType.Byte)
                    {
                        newBytePropertyData.Value = bytePropertyData.Value;
                    }
                    else
                    {
                        FString byteValueName = originalUAsset.GetNameReference(bytePropertyData.Value);
                        attachToAsset.AddNameReference(byteValueName);
                        newBytePropertyData.EnumValue = FName.FromString(attachToAsset, bytePropertyData.EnumValue.ToString());
                    }
                    if (bytePropertyData.EnumType != null)
                    {
                        FString byteEnumTypeName = originalUAsset.GetNameReference(
                            originalUAsset.SearchNameReference(bytePropertyData.EnumType.Value)
                        );
                        attachToAsset.AddNameReference(byteEnumTypeName);
                        newBytePropertyData.EnumType = FName.FromString(attachToAsset, byteEnumTypeName.ToString());
                    }
                    newPropertyDataList.Add(newBytePropertyData);
                }
                else if (propertyData is DelegatePropertyData delegatePropertyData)
                {
                    DelegatePropertyData newDelegatePropertyData = new DelegatePropertyData(newPropertyName);
                    int newObjectIndex = delegatePropertyData.Value.Object.Index - 1;
                    if (UsedExports != null)
                    {
                        newObjectIndex = UsedExports.IndexOf(delegatePropertyData.Value.Object.Index - 1);
                    }
                    if (newObjectIndex != -1)
                    {
                        newObjectIndex += exportStartIndex + 1;
                    }
                    else
                    {
                        newObjectIndex = 0;
                    }
                    newDelegatePropertyData.Value = new FDelegate(
                        FPackageIndex.FromRawIndex(newObjectIndex),
                        FName.FromString(attachToAsset, delegatePropertyData.Value.Delegate.Value.Value)
                    );
                    newPropertyDataList.Add(newDelegatePropertyData);
                }
                else if (propertyData is EnumPropertyData enumPropertyData)
                {
                    EnumPropertyData newEnumPropertyData = new EnumPropertyData(newPropertyName);
                    // FName newEnumValue = new FName(attachToAsset, enumPropertyData.Value.Value.Value, enumPropertyData.Value.Number);
                    // FName newEnumType = new FName(attachToAsset, enumPropertyData.EnumType.Value.Value, enumPropertyData.EnumType.Number);
                    // attachToAsset.AddNameReference(newEnumValue.Value);
                    // attachToAsset.AddNameReference(newEnumType.Value);
                    FName newEnumValue = FName.FromString(attachToAsset, enumPropertyData.Value.Value.Value);
                    FName newEnumType = FName.FromString(attachToAsset, enumPropertyData.EnumType.Value.Value);
                    newEnumPropertyData.Value = newEnumValue;
                    newEnumPropertyData.EnumType = newEnumType;
                    newPropertyDataList.Add(newEnumPropertyData);
                }
                else if (propertyData is FloatPropertyData floatPropertyData)
                {
                    FloatPropertyData newFloatPropertyData = new FloatPropertyData(newPropertyName);
                    newFloatPropertyData.Value = floatPropertyData.Value;
                    newPropertyDataList.Add(newFloatPropertyData);
                }
                else if (propertyData is Int8PropertyData int8PropertyData)
                {
                    Int8PropertyData newInt8PropertyData = new Int8PropertyData(newPropertyName);
                    newInt8PropertyData.Value = int8PropertyData.Value;
                    newPropertyDataList.Add(newInt8PropertyData);
                }
                else if (propertyData is Int16PropertyData int16PropertyData)
                {
                    Int16PropertyData newInt16PropertyData = new Int16PropertyData(newPropertyName);
                    newInt16PropertyData.Value = int16PropertyData.Value;
                    newPropertyDataList.Add(newInt16PropertyData);
                }
                else if (propertyData is Int64PropertyData int64PropertyData)
                {
                    Int64PropertyData newInt64PropertyData = new Int64PropertyData(newPropertyName);
                    newInt64PropertyData.Value = int64PropertyData.Value;
                    newPropertyDataList.Add(newInt64PropertyData);
                }
                else if (propertyData is IntPropertyData intPropertyData)
                {
                    IntPropertyData newIntPropertyData = new IntPropertyData(newPropertyName);
                    newIntPropertyData.Value = intPropertyData.Value;
                    newPropertyDataList.Add(newIntPropertyData);
                }
                else if (propertyData is MapPropertyData mapPropertyData)
                {
                    newPropertyDataList.Add((MapPropertyData)mapPropertyData.Clone());
                }
                else if (propertyData is MulticastDelegatePropertyData multicastDelegatePropertyData)
                {
                    MulticastDelegatePropertyData newMulticastDelegatePropertyData = new MulticastDelegatePropertyData(newPropertyName);
                    FMulticastDelegate[] newValue = new FMulticastDelegate[multicastDelegatePropertyData.Value.Length];
                    for (int i = 0; i < multicastDelegatePropertyData.Value.Length; i++)
                    {
                        // attachToAsset.AddNameReference(multicastDelegatePropertyData.Value[i].Delegate.Value);
                        int newNumberIndex = multicastDelegatePropertyData.Value[i].Number - 1;
                        if (UsedExports != null)
                        {
                            newNumberIndex = UsedExports.IndexOf(multicastDelegatePropertyData.Value[i].Number - 1);
                        }
                        if (newNumberIndex != -1)
                        {
                            newNumberIndex += exportStartIndex + 1;
                        }
                        else
                        {
                            newNumberIndex = 0;
                        }
                        newValue[i] = new FMulticastDelegate(
                            newNumberIndex,
                            FName.FromString(attachToAsset, multicastDelegatePropertyData.Value[i].Delegate.Value.Value)
                        // new FName(attachToAsset, multicastDelegatePropertyData.Value[i].Delegate.Value.Value, multicastDelegatePropertyData.Value[i].Delegate.Number)
                        );
                    }
                    newMulticastDelegatePropertyData.Value = newValue;
                    newPropertyDataList.Add(newMulticastDelegatePropertyData);
                }
                else if (propertyData is NamePropertyData namePropertyData)
                {
                    NamePropertyData newNamePropertyData = new NamePropertyData(newPropertyName);
                    // attachToAsset.AddNameReference(namePropertyData.Value.Value);
                    // newNamePropertyData.Value = new FName(attachToAsset, namePropertyData.Value.Value.Value, namePropertyData.Value.Number);
                    newNamePropertyData.Value = FName.FromString(attachToAsset, namePropertyData.Value.Value.Value);
                    newPropertyDataList.Add(newNamePropertyData);
                }
                else if (propertyData is ObjectPropertyData objectPropertyData)
                {
                    ObjectPropertyData newObjectPropertyData = new ObjectPropertyData(newPropertyName);
                    bool isImport = objectPropertyData.Value.IsImport();
                    bool isExport = objectPropertyData.Value.IsExport();
                    int newCurrentIndex = Math.Abs(objectPropertyData.Value.Index) - 1;
                    if (isExport)
                    {
                        if (UsedExports != null)
                        {
                            newCurrentIndex = UsedExports.IndexOf(objectPropertyData.Value.Index - 1);
                        }
                        newCurrentIndex += exportStartIndex + 1;
                    }
                    else if (isImport)
                    {
                        if (UsedImports != null)
                        {
                            int usedImportIndex = UsedImports.IndexOf(newCurrentIndex);
                            if (usedImportIndex > -1)
                            {
                                newCurrentIndex = -(mappedImports[usedImportIndex] + 1);
                            }
                        }
                        else
                        {
                            newCurrentIndex = -(mappedImports[newCurrentIndex] + 1);
                        }
                    }
                    else
                    {
                        newCurrentIndex = 0;
                    }
                    newObjectPropertyData.Value = FPackageIndex.FromRawIndex(newCurrentIndex);
                    newPropertyDataList.Add(newObjectPropertyData);
                }
                else if (propertyData is SetPropertyData setPropertyData)
                {
                    SetPropertyData newSetPropertyData = new SetPropertyData(newPropertyName);
                    newSetPropertyData.Value = ClonePropertyData(originalUAsset, setPropertyData.Value.ToList<PropertyData>(), attachToAsset, exportStartIndex, mappedImports).ToArray();
                    newPropertyDataList.Add(newSetPropertyData);
                }
                else if (propertyData is SoftAssetPathPropertyData softAssetPathPropertyData)
                {
                    newPropertyDataList.Add((SoftAssetPathPropertyData)softAssetPathPropertyData.Clone());
                }
                else if (propertyData is SoftClassPathPropertyData softClassPathPropertyData)
                {
                    newPropertyDataList.Add((SoftClassPathPropertyData)softClassPathPropertyData.Clone());
                }
                else if (propertyData is SoftObjectPropertyData softObjectPropertyData)
                {
                    newPropertyDataList.Add((SoftObjectPropertyData)softObjectPropertyData.Clone());
                }
                else if (propertyData is StrPropertyData strPropertyData)
                {
                    StrPropertyData newStrPropertyData = new StrPropertyData(newPropertyName);
                    newStrPropertyData.Value = strPropertyData.Value;
                    newPropertyDataList.Add(newStrPropertyData);
                }
                else if (propertyData is TextPropertyData textPropertyData)
                {
                    TextPropertyData newTextPropertyData = new TextPropertyData(newPropertyName);
                    newTextPropertyData.Value = new FString(textPropertyData.Value.Value, textPropertyData.Value.Encoding);
                    newTextPropertyData.Flags = textPropertyData.Flags;
                    newTextPropertyData.HistoryType = textPropertyData.HistoryType;
                    if (textPropertyData.TableId != null)
                    {
                        attachToAsset.AddNameReference(textPropertyData.TableId.Value);
                        // newTextPropertyData.TableId = new FName(attachToAsset, textPropertyData.TableId.Value.Value, textPropertyData.TableId.Number);
                        newTextPropertyData.TableId = FName.FromString(attachToAsset, textPropertyData.TableId.Value.Value);
                    }
                    if (textPropertyData.Namespace != null)
                    {
                        attachToAsset.AddNameReference(textPropertyData.Namespace);
                        newTextPropertyData.Namespace = new FString(textPropertyData.Namespace.Value, textPropertyData.Namespace.Encoding);
                    }
                    if (textPropertyData.CultureInvariantString != null)
                    {
                        attachToAsset.AddNameReference(textPropertyData.CultureInvariantString);
                        newTextPropertyData.CultureInvariantString = new FString(textPropertyData.CultureInvariantString.Value, textPropertyData.CultureInvariantString.Encoding);
                    }
                    newPropertyDataList.Add(newTextPropertyData);
                }
                else if (propertyData is UInt16PropertyData uInt16PropertyData)
                {
                    UInt16PropertyData newUInt16PropertyData = new UInt16PropertyData(newPropertyName);
                    newUInt16PropertyData.Value = uInt16PropertyData.Value;
                    newPropertyDataList.Add(newUInt16PropertyData);
                }
                else if (propertyData is UInt32PropertyData uInt32PropertyData)
                {
                    UInt32PropertyData newUInt32PropertyData = new UInt32PropertyData(newPropertyName);
                    newUInt32PropertyData.Value = uInt32PropertyData.Value;
                    newPropertyDataList.Add(newUInt32PropertyData);
                }
                else if (propertyData is UInt64PropertyData uInt64PropertyData)
                {
                    UInt64PropertyData newUInt64PropertyData = new UInt64PropertyData(newPropertyName);
                    newUInt64PropertyData.Value = uInt64PropertyData.Value;
                    newPropertyDataList.Add(newUInt64PropertyData);
                }
                else if (propertyData is UnknownPropertyData unknownPropertyData)
                {
                    UnknownPropertyData newUnknownPropertyData = new UnknownPropertyData(newPropertyName);
                    newUnknownPropertyData.Value = unknownPropertyData.Value;
                    newPropertyDataList.Add(newUnknownPropertyData);
                }
                else if (propertyData is BoxPropertyData boxPropertyData)
                {
                    BoxPropertyData newBoxPropertyData = new BoxPropertyData(newPropertyName);
                    newBoxPropertyData.Value = (VectorPropertyData[])ClonePropertyData(originalUAsset, boxPropertyData.Value.ToList<PropertyData>(), attachToAsset, exportStartIndex, mappedImports).ToArray();
                    newBoxPropertyData.IsValid = boxPropertyData.IsValid;
                    newPropertyDataList.Add(newBoxPropertyData);
                }
                else if (propertyData is ColorPropertyData colorPropertyData)
                {
                    ColorPropertyData newColorPropertyData = new ColorPropertyData(newPropertyName);
                    newColorPropertyData.Value = System.Drawing.Color.FromArgb(colorPropertyData.Value.A, colorPropertyData.Value.R, colorPropertyData.Value.G, colorPropertyData.Value.B);
                    newPropertyDataList.Add(newColorPropertyData);
                }
                else if (propertyData is DateTimePropertyData dateTimePropertyData)
                {
                    DateTimePropertyData newDateTimePropertyData = new DateTimePropertyData(newPropertyName);
                    newDateTimePropertyData.Value = dateTimePropertyData.Value;
                    newPropertyDataList.Add(newDateTimePropertyData);
                }
                else if (propertyData is GameplayTagContainerPropertyData gameplayTagContainerPropertyData)
                {
                    GameplayTagContainerPropertyData newGameplayTagContainerPropertyData = new GameplayTagContainerPropertyData(newPropertyName);
                    FName[] newData = new FName[gameplayTagContainerPropertyData.Value.Length];
                    for (int i = 0; i < gameplayTagContainerPropertyData.Value.Length; i++)
                    {
                        newData[i] = FName.FromString(attachToAsset, gameplayTagContainerPropertyData.Value[i].ToString());
                    }
                    newGameplayTagContainerPropertyData.Value = newData;
                    newPropertyDataList.Add(newGameplayTagContainerPropertyData);
                }
                else if (propertyData is GuidPropertyData guidPropertyData)
                {
                    GuidPropertyData newGuidPropertyData = new GuidPropertyData(newPropertyName);
                    newGuidPropertyData.Value = guidPropertyData.Value;
                    newPropertyDataList.Add(newGuidPropertyData);
                }
                else if (propertyData is IntPointPropertyData intPointPropertyData)
                {
                    IntPointPropertyData newIntPointPropertyData = new IntPointPropertyData(newPropertyName);
                    int[] newValue = new int[intPointPropertyData.Value.Length];
                    intPointPropertyData.Value.CopyTo(newValue, 0);
                    newIntPointPropertyData.Value = newValue;
                    newPropertyDataList.Add(newIntPointPropertyData);
                }
                else if (propertyData is LinearColorPropertyData linearColorPropertyData)
                {
                    LinearColorPropertyData newLinearColorPropertyData = new LinearColorPropertyData(newPropertyName);
                    newLinearColorPropertyData.Value = new LinearColor(linearColorPropertyData.Value.R, linearColorPropertyData.Value.G, linearColorPropertyData.Value.B, linearColorPropertyData.Value.A);
                    newPropertyDataList.Add(newLinearColorPropertyData);
                }
                else if (propertyData is ExpressionInputPropertyData expressionInputPropertyData)
                {
                    newPropertyDataList.Add((ExpressionInputPropertyData)expressionInputPropertyData.Clone());
                }
                else if (propertyData is MaterialAttributesInputPropertyData materialAttributesInputPropertyData)
                {
                    newPropertyDataList.Add((MaterialAttributesInputPropertyData)materialAttributesInputPropertyData.Clone());
                }
                else if (propertyData is ColorMaterialInputPropertyData colorMaterialInputPropertyData)
                {
                    newPropertyDataList.Add((ColorMaterialInputPropertyData)colorMaterialInputPropertyData.Clone());
                }
                else if (propertyData is ScalarMaterialInputPropertyData scalarMaterialInputPropertyData)
                {
                    newPropertyDataList.Add((ScalarMaterialInputPropertyData)scalarMaterialInputPropertyData.Clone());
                }
                else if (propertyData is ShadingModelMaterialInputPropertyData shadingModelMaterialInputPropertyData)
                {
                    newPropertyDataList.Add((ShadingModelMaterialInputPropertyData)shadingModelMaterialInputPropertyData.Clone());
                }
                else if (propertyData is VectorMaterialInputPropertyData vectorMaterialInputPropertyData)
                {
                    newPropertyDataList.Add((VectorMaterialInputPropertyData)vectorMaterialInputPropertyData.Clone());
                }
                else if (propertyData is Vector2MaterialInputPropertyData vector2MaterialInputPropertyData)
                {
                    newPropertyDataList.Add((Vector2MaterialInputPropertyData)vector2MaterialInputPropertyData.Clone());
                }
                else if (propertyData is PerPlatformBoolPropertyData perPlatformBoolPropertyData)
                {
                    PerPlatformBoolPropertyData newPerPlatformBoolPropertyData = new PerPlatformBoolPropertyData(newPropertyName);
                    bool[] newValue = new bool[perPlatformBoolPropertyData.Value.Length];
                    perPlatformBoolPropertyData.Value.CopyTo(newValue, 0);
                    newPerPlatformBoolPropertyData.Value = newValue;
                    newPropertyDataList.Add(newPerPlatformBoolPropertyData);
                }
                else if (propertyData is PerPlatformFloatPropertyData perPlatformFloatPropertyData)
                {
                    PerPlatformFloatPropertyData newPerPlatformFloatPropertyData = new PerPlatformFloatPropertyData(newPropertyName);
                    float[] newValue = new float[perPlatformFloatPropertyData.Value.Length];
                    perPlatformFloatPropertyData.Value.CopyTo(newValue, 0);
                    newPerPlatformFloatPropertyData.Value = newValue;
                    newPropertyDataList.Add(newPerPlatformFloatPropertyData);
                }
                else if (propertyData is QuatPropertyData quatPropertyData)
                {
                    newPropertyDataList.Add((QuatPropertyData)quatPropertyData.Clone());
                }
                else if (propertyData is RichCurveKeyPropertyData richCurveKeyPropertyData)
                {
                    newPropertyDataList.Add((RichCurveKeyPropertyData)richCurveKeyPropertyData.Clone());
                }
                else if (propertyData is RotatorPropertyData rotatorPropertyData)
                {
                    newPropertyDataList.Add((RotatorPropertyData)rotatorPropertyData.Clone());
                }
                else if (propertyData is StructPropertyData structPropertyData)
                {
                    StructPropertyData newStructPropertyData = new StructPropertyData(newPropertyName);
                    if (structPropertyData.StructType != null)
                    {
                        newStructPropertyData.StructType = FName.FromString(attachToAsset, structPropertyData.StructType.Value.ToString());
                    }
                    newStructPropertyData.SerializeNone = structPropertyData.SerializeNone;
                    newStructPropertyData.StructGUID = structPropertyData.StructGUID;
                    newStructPropertyData.Value = ClonePropertyData(
                        originalUAsset,
                        structPropertyData.Value,
                        attachToAsset,
                        exportStartIndex,
                        mappedImports
                    );
                    newPropertyDataList.Add(newStructPropertyData);
                }
                else if (propertyData is TimespanPropertyData timespanPropertyData)
                {
                    TimespanPropertyData newTimespanPropertyData = new TimespanPropertyData(newPropertyName);
                    newTimespanPropertyData.Value = timespanPropertyData.Value;
                    newPropertyDataList.Add(newTimespanPropertyData);
                }
                else if (propertyData is Vector2DPropertyData vector2DPropertyData)
                {
                    newPropertyDataList.Add((Vector2DPropertyData)vector2DPropertyData.Clone());
                }
                else if (propertyData is Vector4PropertyData vector4PropertyData)
                {
                    newPropertyDataList.Add((Vector4PropertyData)vector4PropertyData.Clone());
                }
                else if (propertyData is VectorPropertyData vectorPropertyData)
                {
                    newPropertyDataList.Add((VectorPropertyData)vectorPropertyData.Clone());
                }
                else if (propertyData is ViewTargetBlendParamsPropertyData viewTargetBlendParamsPropertyData)
                {
                    ViewTargetBlendParamsPropertyData newViewTargetBlendParamsPropertyData = new ViewTargetBlendParamsPropertyData(newPropertyName);
                    newViewTargetBlendParamsPropertyData.BlendTime = viewTargetBlendParamsPropertyData.BlendTime;
                    newViewTargetBlendParamsPropertyData.BlendFunction = viewTargetBlendParamsPropertyData.BlendFunction;
                    newViewTargetBlendParamsPropertyData.BlendExp = viewTargetBlendParamsPropertyData.BlendExp;
                    newViewTargetBlendParamsPropertyData.bLockOutgoing = viewTargetBlendParamsPropertyData.bLockOutgoing;
                    newPropertyDataList.Add(newViewTargetBlendParamsPropertyData);
                }
            }
            return newPropertyDataList;
        }

    }
}