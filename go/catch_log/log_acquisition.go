/*
 Package main provides Asynchronous log acquisition
  author: t.yonesaka
*/
package main

import (
    "sync"
    "log"
    "os"
    "io"
    "io/ioutil"
    "path/filepath"
    "gopkg.in/yaml.v2"
    "./data"
    "./operation"
    "./constant"
)

func main() {
    fileName := operation.GetLogFineName()
    logfile, err := os.OpenFile(fileName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
    if err != nil {
        panic("cannnot open log files:" + err.Error())
    }
    defer logfile.Close()
    log.SetOutput(io.MultiWriter(logfile, os.Stdout))
    log.SetFlags(log.Ldate | log.Ltime)

    // Read the configuration file
    log.Println("Log Acquisition - Start -")

    dir, err := filepath.Abs(filepath.Dir(os.Args[0]))
    if err != nil {
       panic(err)
    }
    log.Println(dir)

    buf, err := ioutil.ReadFile(dir + "/config/host_setting.yml")
    if err != nil {
        panic(err)
    }

    // Convert configuration file to structure
    hosts := []data.Host{}
    err = yaml.Unmarshal(buf, &hosts)

    // Perform processing asynchronously(MaxProcess:7)
    var wg sync.WaitGroup
    semaphore := make(chan int, constant.MaxProcess)
    for _, host := range hosts {
        wg.Add(1)
        go func(hostData data.Host) {
            defer wg.Done()
            semaphore <- 1
            log.Println("Host: " + hostData.Name + " - start -")
            operation.RsyncExec(hostData)
            log.Println("Host: " + hostData.Name + " - end -")
            <- semaphore
        }(host)
    }
    wg.Wait()
    log.Println("Log Acquisition - End -")
}
