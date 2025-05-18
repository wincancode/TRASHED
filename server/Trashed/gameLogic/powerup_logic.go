package gameLogic

import (
	"fmt"
	"math/rand"
	"time"
)

// PowerUp representa un potenciador en el juego
type PowerUp struct {
	PosX   float64
	PosY   float64
	Type   string // Tipo de potenciador (e.g., "laser_boost", "shield")
	Width  int
	Height int
	Active bool
}

// InitializePowerUp crea un nuevo potenciador
func InitializePowerUp(x, y float64, powerType string) PowerUp {
	return PowerUp{
		PosX:   x,
		PosY:   y,
		Type:   powerType,
		Width:  100, // Ancho del texto
		Height: 30,  // Altura del texto
		Active: true,
	}
}

// ApplyPowerUpEffect aplica el efecto del potenciador a la nave
func ApplyPowerUpEffect(ship *ShipState, powerUp *PowerUp, messages *[]string) {
	switch powerUp.Type {
	case "laser_boost":
		ship.LaserBoostLevel++
		*messages = append(*messages, formatMessage("Láser mejorado: Nivel %d", ship.LaserBoostLevel))
	case "shield":
		ship.ShieldCharges++
		ship.ShieldActive = true
		*messages = append(*messages, formatMessage("Escudo mejorado: %d cargas", ship.ShieldCharges))
	}
	powerUp.Active = false
}

// CheckPowerUpCollision verifica si la nave recoge un potenciador
func CheckPowerUpCollision(ship *ShipState, powerUp *PowerUp) bool {
	shipLeft := ship.PosX - 25 // Asumiendo un ancho fijo de 50 para la nave
	shipRight := ship.PosX + 25
	shipTop := ship.PosY - 25
	shipBottom := ship.PosY + 25

	powerUpLeft := powerUp.PosX - float64(powerUp.Width)/2
	powerUpRight := powerUp.PosX + float64(powerUp.Width)/2
	powerUpTop := powerUp.PosY - float64(powerUp.Height)/2
	powerUpBottom := powerUp.PosY + float64(powerUp.Height)/2

	return !(shipRight < powerUpLeft || shipLeft > powerUpRight || shipBottom < powerUpTop || shipTop > powerUpBottom)
}

// GenerateRandomPowerUp genera un potenciador aleatorio en una posición específica
func GenerateRandomPowerUp(x, y float64) PowerUp {
	rand.Seed(time.Now().UnixNano())
	powerTypes := []string{"laser_boost", "shield"}
	randomType := powerTypes[rand.Intn(len(powerTypes))]
	return InitializePowerUp(x, y, randomType)
}

// formatMessage genera un mensaje con formato para los efectos de los power-ups
func formatMessage(text string, value int) string {
	return fmt.Sprintf(text, value)
}
