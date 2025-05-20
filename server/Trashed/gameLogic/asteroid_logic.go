package gameLogic

import (
	"math"
	"math/rand"
	"time"
)

// Asteroid representa un asteroide en el juego
type Asteroid struct {
	ID        int
	PosX      float64
	PosY      float64
	Width     int
	Height    int
	Speed     float64
	Angle     float64
	Health    int
	MaxHealth int
}

// InitializeAsteroid genera un nuevo asteroide con propiedades aleatorias
func InitializeAsteroid(id int, difficultyFactor int) Asteroid {

	//asteroids can only spawn from the edges of the screen

	posX := float64(rand.Intn(800)) // Ejemplo: ancho del juego
	posY := float64(rand.Intn(600)) // Ejemplo: alto del juego

	if rand.Intn(2) == 0 {
		posX = 0
		posY = float64(rand.Intn(600))
	} else {
		posX = float64(rand.Intn(800))
		posY = 0
	}

	
	
	

	rand.Seed(time.Now().UnixNano())
	baseSize := rand.Intn(30) + 20
	return Asteroid{
		ID:        id,
		Width:     baseSize + difficultyFactor*5,
		Height:    baseSize + difficultyFactor*5,
		PosX:      float64(posX), // Ejemplo: ancho del juego
		PosY:      float64(posY), // Ejemplo: alto del juego
		Speed:     rand.Float64()*100 + 50,
		Angle:     rand.Float64() * 360,
		Health:    (baseSize / 10) + difficultyFactor,
		MaxHealth: (baseSize / 10) + difficultyFactor,
	}
}

// UpdateAsteroidPosition actualiza la posición del asteroide
func UpdateAsteroidPosition(asteroid *Asteroid, deltaTime float64, gameWidth, gameHeight int) {
	asteroid.PosX += asteroid.Speed * math.Cos(asteroid.Angle*math.Pi/180) * deltaTime
	asteroid.PosY += asteroid.Speed * math.Sin(asteroid.Angle*math.Pi/180) * deltaTime
	// Hacer que el asteroide aparezca en el lado opuesto si sale de los límites
	if asteroid.PosX < 0 {
		asteroid.PosX = float64(gameWidth)
	}
	if asteroid.PosX > float64(gameWidth) {
		asteroid.PosX = 0
	}
	if asteroid.PosY < 0 {
		asteroid.PosY = float64(gameHeight)
	}
	if asteroid.PosY > float64(gameHeight) {
		asteroid.PosY = 0
	}
	
}

