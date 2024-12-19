from excel import generateDiffReports, mergeReports


if __name__ == '__main__':
    #file1Path = "echo.xlsx"
    #file2Path = "echo.xlsx"
    
    #mergeReports(file1Path, file2Path)
    file1Path = "echo.xlsx"
    file2Path = "pass.xlsx"
    
    generateDiffReports(file1Path, file2Path)