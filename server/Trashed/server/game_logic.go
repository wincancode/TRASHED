package main

import (
	"fmt"
	"sync"
)

// GameState representa el estado global del juego
type GameState struct {
	Players           map[string]*ShipState // Mapa de jugadores conectados (UUID -> ShipState)
	Level             Level                 // Estado del nivel actual
	Asteroids         []Asteroid            // Lista de asteroides activos
	PowerUps          []PowerUp             // Lista de power-ups activos
	ReleasedAsteroids []Asteroid            // Asteroides secundarios liberados
	Messages          []Event               // Mensajes temporales
	ScoreBoard        []PlayerScore         // Tabla de puntuaciones
	Mutex             sync.Mutex            // Mutex para sincronizar el acceso al estado del juego
	GameOver          bool                  // Indica si el juego ha terminado
}

// InitializeGameState inicializa el estado del juego
func InitializeGameState() *GameState {
	return &GameState{
		Players:           make(map[string]*ShipState),
		Level:             InitializeLevel(),
		Asteroids:         []Asteroid{},
		PowerUps:          []PowerUp{},
		ReleasedAsteroids: []Asteroid{},
		Messages:          []Event{},
		ScoreBoard:        []PlayerScore{},
		GameOver:          false,
	}
}

// AddPlayer agrega un nuevo jugador al juego
func AddPlayer(state *GameState, playerUUID string, color string) {
	state.Mutex.Lock()
	defer state.Mutex.Unlock()

	// Crear una nueva nave para el jugador
	ship := &ShipState{
		PlayerUuid:      playerUUID,
		PosX:            400, // Posición inicial
		PosY:            300,
		Angle:           0,
		Speed:           0,
		LaserBoostLevel: 0,
		ShieldActive:    false,
		ShieldCharges:   0,
		Lives:           3,
	}
	state.Players[playerUUID] = ship
	fmt.Printf("Jugador %s conectado.\n", playerUUID)
}

// RemovePlayer elimina un jugador del juego
func RemovePlayer(state *GameState, playerUUID string) {
	state.Mutex.Lock()
	defer state.Mutex.Unlock()

	delete(state.Players, playerUUID)
	fmt.Printf("Jugador %s desconectado.\n", playerUUID)
}

// SyncGameState sincroniza el estado del juego con los clientes
func SyncGameState(state *GameState) {
	state.Mutex.Lock()
	defer state.Mutex.Unlock()

	// Enviar el estado del juego a todos los clientes conectados
	for _, player := range state.Players {
		fmt.Printf("Sincronizando estado para el jugador %s: PosX=%.2f, PosY=%.2f\n", player.PlayerUuid, player.PosX, player.PosY)
	}
}

// CheckGameOver verifica si el juego ha terminado
func CheckGameOver(state *GameState) bool {
	state.Mutex.Lock()
	defer state.Mutex.Unlock()

	// El juego termina si todos los jugadores pierden sus vidas
	for _, player := range state.Players {
		if player.Lives > 0 {
			return false
		}
	}
	state.GameOver = true
	return true
}

// HandleGameOver maneja la lógica de fin de juego
func HandleGameOver(state *GameState) {
	if state.GameOver {
		fmt.Println("¡El juego ha terminado!")
		// Enviar un mensaje de "Game Over" a todos los clientes
		for _, player := range state.Players {
			fmt.Printf("Jugador %s: Game Over\n", player.PlayerUuid)
		}
	}
}
