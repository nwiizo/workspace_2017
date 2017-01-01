rule Base64
{
    strings:
        $a = /([A-Za-z0-9+\/]{4}){3,}([A-Za-z0-9+\/]{2}==|[A-Za-z0-9+\/]{3}=)?/
    condition:
        $a
}
