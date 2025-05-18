package main

import "fmt"

// Event representa un evento importante en el juego
type Event struct {
	Message string  // Mensaje del evento
	PosX    float64 // Posición X donde ocurrió el evento
	PosY    float64 // Posición Y donde ocurrió el evento
	Timer   float64 // Duración del mensaje en segundos
	Opacity float64 // Opacidad del mensaje (para efectos visuales)
}

// CreateEvent crea un nuevo evento
func CreateEvent(message string, x, y float64) Event {
	return Event{
		Message: message,
		PosX:    x,
		PosY:    y,
		Timer:   3.0, // Mostrar el mensaje durante 3 segundos
		Opacity: 255, // Opacidad inicial
	}
}

// UpdateEvents actualiza los eventos activos (reduce el tiempo y opacidad)
func UpdateEvents(events *[]Event, deltaTime float64) {
	for i := 0; i < len(*events); i++ {
		event := &(*events)[i]
		event.Timer -= deltaTime
		event.PosY -= 50 * deltaTime // Mover el mensaje hacia arriba
		event.Opacity -= 85 * deltaTime

		// Eliminar eventos que hayan expirado
		if event.Timer <= 0 || event.Opacity <= 0 {
			*events = append((*events)[:i], (*events)[i+1:]...)
			i-- // Ajustar el índice después de eliminar
		}
	}
}

// HandleLevelUpEvent maneja el evento de subir de nivel
func HandleLevelUpEvent(events *[]Event, level *Level, screenWidth, screenHeight float64) {
	message := fmt.Sprintf("¡Subiste al Nivel %d!", level.CurrentLevel)
	*events = append(*events, CreateEvent(message, screenWidth/2, screenHeight/2))
}

// HandlePowerUpEvent maneja el evento de recoger un power-up
func HandlePowerUpEvent(events *[]Event, powerUpType string, ship *ShipState) {
	var message string
	switch powerUpType {
	case "laser_boost":
		message = fmt.Sprintf("Láser mejorado: Nivel %d", ship.LaserBoostLevel)
	case "shield":
		message = fmt.Sprintf("Escudo mejorado: %d cargas", ship.ShieldCharges)
	}
	*events = append(*events, CreateEvent(message, ship.PosX, ship.PosY-50))
}

// HandleAsteroidDestroyedEvent maneja el evento de destruir un asteroide
func HandleAsteroidDestroyedEvent(events *[]Event, points int, asteroid *Asteroid) {
	message := fmt.Sprintf("+%d puntos", points)
	*events = append(*events, CreateEvent(message, asteroid.PosX, asteroid.PosY))
}
