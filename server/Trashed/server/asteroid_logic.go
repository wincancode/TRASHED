package main

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
	rand.Seed(time.Now().UnixNano())
	baseSize := rand.Intn(30) + 20
	return Asteroid{
		ID:        id,
		Width:     baseSize + difficultyFactor*5,
		Height:    baseSize + difficultyFactor*5,
		PosX:      float64(rand.Intn(800)), // Ejemplo: ancho del juego
		PosY:      float64(rand.Intn(600)), // Ejemplo: alto del juego
		Speed:     rand.Float64()*100 + 50,
		Angle:     rand.Float64() * 360,
		Health:    (baseSize / 10) + difficultyFactor,
		MaxHealth: (baseSize / 10) + difficultyFactor,
	}
}

// UpdateAsteroidPosition actualiza la posición del asteroide
func UpdateAsteroidPosition(asteroid *Asteroid, deltaTime float64) {
	asteroid.PosX += asteroid.Speed * math.Cos(asteroid.Angle*math.Pi/180) * deltaTime
	asteroid.PosY += asteroid.Speed * math.Sin(asteroid.Angle*math.Pi/180) * deltaTime
}
