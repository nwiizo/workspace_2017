/*
 Package data provides simple strcut
 Store data of yml file
  author: t.yonesaka
*/
package data

type Host struct{
    Name string `yaml:"name"`
    Address string `yaml:"address"`
    Port string `yaml:"port"`
    LogSettings []LogSetting `yaml:"log_setting"`
}

type LogSetting struct{
    LogDir string `yaml:"log_dir"`
    Include []string `yaml:include`
}
