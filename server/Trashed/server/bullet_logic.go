package main

import (
	"math"
)

// Bullet representa una bala en el juego
type Bullet struct {
	PosX   float64
	PosY   float64
	Angle  float64
	Speed  float64
	Active bool
	Damage int
	Width  int
	Height int
}

// InitializeBullet crea una nueva bala
func InitializeBullet(x, y, angle float64, laserBoostLevel int) Bullet {
	const baseSpeed = 300.0 // Velocidad base de la bala
	const baseDamage = 1    // Daño base de la bala

	return Bullet{
		PosX:   x,
		PosY:   y,
		Angle:  angle,
		Speed:  baseSpeed,
		Active: true,
		Damage: baseDamage + laserBoostLevel,
		Width:  5,  // Ancho de la bala
		Height: 10, // Alto de la bala
	}
}

// UpdateBulletPosition actualiza la posición de la bala
func UpdateBulletPosition(bullet *Bullet, deltaTime float64, gameWidth, gameHeight int) {
	bullet.PosX += bullet.Speed * math.Sin(bullet.Angle*math.Pi/180) * deltaTime
	bullet.PosY -= bullet.Speed * math.Cos(bullet.Angle*math.Pi/180) * deltaTime

	// Desactivar la bala si sale de los límites del juego
	if bullet.PosX < 0 || bullet.PosX > float64(gameWidth) || bullet.PosY < 0 || bullet.PosY > float64(gameHeight) {
		bullet.Active = false
	}
}

// CheckBulletAsteroidCollision verifica si una bala colisiona con un asteroide
func CheckBulletAsteroidCollision(bullet *Bullet, asteroid *Asteroid) bool {
	bulletLeft := bullet.PosX - float64(bullet.Width)/2
	bulletRight := bullet.PosX + float64(bullet.Width)/2
	bulletTop := bullet.PosY - float64(bullet.Height)/2
	bulletBottom := bullet.PosY + float64(bullet.Height)/2

	asteroidLeft := asteroid.PosX - float64(asteroid.Width)/2
	asteroidRight := asteroid.PosX + float64(asteroid.Width)/2
	asteroidTop := asteroid.PosY - float64(asteroid.Height)/2
	asteroidBottom := asteroid.PosY + float64(asteroid.Height)/2

	return !(bulletRight < asteroidLeft || bulletLeft > asteroidRight || bulletBottom < asteroidTop || bulletTop > asteroidBottom)
}

// HandleBulletAsteroidCollisions maneja las colisiones entre balas y asteroides
func HandleBulletAsteroidCollisions(bullets *[]Bullet, asteroids *[]Asteroid) (int, int) {
	totalPoints := 0
	destroyedCount := 0

	for i := 0; i < len(*bullets); i++ {
		bullet := &(*bullets)[i]
		if !bullet.Active {
			continue
		}

		for j := 0; j < len(*asteroids); j++ {
			asteroid := &(*asteroids)[j]
			if CheckBulletAsteroidCollision(bullet, asteroid) {
				bullet.Active = false
				asteroid.Health -= bullet.Damage

				if asteroid.Health <= 0 {
					// Eliminar el asteroide
					*asteroids = append((*asteroids)[:j], (*asteroids)[j+1:]...)
					destroyedCount++

					// Calcular puntos según el tamaño del asteroide
					points := asteroid.Width
					totalPoints += points
				}
				break
			}
		}
	}

	return totalPoints, destroyedCount
}
