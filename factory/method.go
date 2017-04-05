package factory


type FactoryMethod struct {
	creators map[uint8] Creator	
}


func (factory *FactoryMethod) AddAction(packettype uint8, creator *Creator, action *Action) {
    
}

func (factory *FactoryMethod) RunAction(data []byte) {
    
}


func (factory *FactoryMethod) Tmp() {
    
}

