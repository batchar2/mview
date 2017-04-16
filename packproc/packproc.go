package packproc

// функции обратного вызова

type CallbackSetDataAction func(data []byte, length uint32)
type CallbackGetDataAction func() ([]byte, uint32)

// Выполнить операцию с данными
type CallbackProcessingData func(data []byte, length uint32) ([]byte, uint32)
