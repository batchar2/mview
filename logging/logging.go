package logging


import (
    "os"
    "log"
)


var (
    Trace   *log.Logger
    Info    *log.Logger
    Warning *log.Logger
    Error   *log.Logger
)


func Init() {
    Trace = log.New(os.Stderr,
        "TRACE: ",
        log.Ldate|log.Ltime|log.Lshortfile)

    Info = log.New(os.Stderr,
        "INFO: ",
        log.Ldate|log.Ltime|log.Lshortfile)

    Warning = log.New(os.Stderr,
        "WARNING: ",
        log.Ldate|log.Ltime|log.Lshortfile)

    Error = log.New(os.Stderr,
        "ERROR: ",
        log.Ldate|log.Ltime|log.Lshortfile)
}
