/*
 Package operation provides solaris commadn functions.
  author: t.yonesaka
*/
package operation

import (
    "os"
    "os/exec"
    "log"
    "time"
    "strings"
    "../data"
    "../constant"
)

// Get logfile name
func GetLogFineName() string {
  time := time.Now()
  layout := "20060102"
  now := time.Format(layout)
  return constant.LogFile + now + ".log"
}

// Set options from host information and execute rsync
func RsyncExec(host data.Host) bool {
    // Create log storage directory for each server
    baseDir := constant.BaseDir + host.Name
    baseRes := makeDir(baseDir)
    if !baseRes {
        return false
    }

    errCount := 0
    for _, logSetting := range host.LogSettings {
       // Create a directory of LogDir variables recursively
       subDir := baseDir + logSetting.LogDir
       subRes := makeDir(subDir)
       if !subRes {
           return false
       }
       // Create rsync options
       options := createOption(host.Address, host.Port, subDir, logSetting.LogDir, logSetting.Include)
       // Exec rsync
       log.Println("rsync " + strings.Join(options," "))
       err, _  := exec.Command("rsync", options...).CombinedOutput()
       if len(err) != 0 {
           log.Println(err)
           errCount++
       }
    }
    if errCount > 0 {
        return false
    }
    return true
}

// Create rsync options
func createOption(address, port, destDir, sourceDir string, list []string) []string{
    options := []string{constant.DefaultOption}
    options = append(options, constant.DefaultIncludeOption)

    for _, include := range list {
        options = append(options, constant.AppendIncludeOption + include)
    }

    options = append(options, constant.DefaultExcludeOption)
    options = append(options, constant.SSHOption + port)
    options = append(options, address + ":" + sourceDir)
    options = append(options, destDir)

    return options
}

// Directory check function
// If the directory does not exist, create it recursively
func makeDir(dirName string) bool {
    _, err := os.Stat(dirName)
    if err != nil {
        mdErr := os.MkdirAll(dirName, 0755)
        return mdErr == nil
    }
    return err == nil
}
