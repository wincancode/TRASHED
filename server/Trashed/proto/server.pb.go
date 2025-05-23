// Code generated by protoc-gen-go. DO NOT EDIT.
// versions:
// 	protoc-gen-go v1.36.6
// 	protoc        v6.30.2
// source: server.proto

package proto

import (
	protoreflect "google.golang.org/protobuf/reflect/protoreflect"
	protoimpl "google.golang.org/protobuf/runtime/protoimpl"
	reflect "reflect"
	sync "sync"
	unsafe "unsafe"
)

const (
	// Verify that this generated code is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(20 - protoimpl.MinVersion)
	// Verify that runtime/protoimpl is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(protoimpl.MaxVersion - 20)
)

type BoolMessage struct {
	state         protoimpl.MessageState `protogen:"open.v1"`
	Value         bool                   `protobuf:"varint,1,opt,name=value,proto3" json:"value,omitempty"`
	unknownFields protoimpl.UnknownFields
	sizeCache     protoimpl.SizeCache
}

func (x *BoolMessage) Reset() {
	*x = BoolMessage{}
	mi := &file_server_proto_msgTypes[0]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *BoolMessage) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*BoolMessage) ProtoMessage() {}

func (x *BoolMessage) ProtoReflect() protoreflect.Message {
	mi := &file_server_proto_msgTypes[0]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use BoolMessage.ProtoReflect.Descriptor instead.
func (*BoolMessage) Descriptor() ([]byte, []int) {
	return file_server_proto_rawDescGZIP(), []int{0}
}

func (x *BoolMessage) GetValue() bool {
	if x != nil {
		return x.Value
	}
	return false
}

type GameCode struct {
	state         protoimpl.MessageState `protogen:"open.v1"`
	Code          string                 `protobuf:"bytes,1,opt,name=code,proto3" json:"code,omitempty"`
	unknownFields protoimpl.UnknownFields
	sizeCache     protoimpl.SizeCache
}

func (x *GameCode) Reset() {
	*x = GameCode{}
	mi := &file_server_proto_msgTypes[1]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *GameCode) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*GameCode) ProtoMessage() {}

func (x *GameCode) ProtoReflect() protoreflect.Message {
	mi := &file_server_proto_msgTypes[1]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use GameCode.ProtoReflect.Descriptor instead.
func (*GameCode) Descriptor() ([]byte, []int) {
	return file_server_proto_rawDescGZIP(), []int{1}
}

func (x *GameCode) GetCode() string {
	if x != nil {
		return x.Code
	}
	return ""
}

type PlayerState struct {
	state         protoimpl.MessageState `protogen:"open.v1"`
	Code          string                 `protobuf:"bytes,1,opt,name=code,proto3" json:"code,omitempty"`
	PlayerUuid    string                 `protobuf:"bytes,2,opt,name=player_uuid,json=playerUuid,proto3" json:"player_uuid,omitempty"`
	Timestamp     int64                  `protobuf:"varint,3,opt,name=timestamp,proto3" json:"timestamp,omitempty"` //For sync
	Input         *Input                 `protobuf:"bytes,5,opt,name=input,proto3" json:"input,omitempty"`
	Position      *Position              `protobuf:"bytes,6,opt,name=position,proto3" json:"position,omitempty"`
	Health        int32                  `protobuf:"varint,7,opt,name=health,proto3" json:"health,omitempty"`
	unknownFields protoimpl.UnknownFields
	sizeCache     protoimpl.SizeCache
}

func (x *PlayerState) Reset() {
	*x = PlayerState{}
	mi := &file_server_proto_msgTypes[2]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *PlayerState) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*PlayerState) ProtoMessage() {}

func (x *PlayerState) ProtoReflect() protoreflect.Message {
	mi := &file_server_proto_msgTypes[2]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use PlayerState.ProtoReflect.Descriptor instead.
func (*PlayerState) Descriptor() ([]byte, []int) {
	return file_server_proto_rawDescGZIP(), []int{2}
}

func (x *PlayerState) GetCode() string {
	if x != nil {
		return x.Code
	}
	return ""
}

func (x *PlayerState) GetPlayerUuid() string {
	if x != nil {
		return x.PlayerUuid
	}
	return ""
}

func (x *PlayerState) GetTimestamp() int64 {
	if x != nil {
		return x.Timestamp
	}
	return 0
}

func (x *PlayerState) GetInput() *Input {
	if x != nil {
		return x.Input
	}
	return nil
}

func (x *PlayerState) GetPosition() *Position {
	if x != nil {
		return x.Position
	}
	return nil
}

func (x *PlayerState) GetHealth() int32 {
	if x != nil {
		return x.Health
	}
	return 0
}

type Position struct {
	state         protoimpl.MessageState `protogen:"open.v1"`
	X             float64                `protobuf:"fixed64,1,opt,name=x,proto3" json:"x,omitempty"`
	Y             float64                `protobuf:"fixed64,2,opt,name=y,proto3" json:"y,omitempty"`
	Angle         float64                `protobuf:"fixed64,3,opt,name=angle,proto3" json:"angle,omitempty"`
	SpeedX        float64                `protobuf:"fixed64,4,opt,name=speedX,proto3" json:"speedX,omitempty"`
	SpeedY        float64                `protobuf:"fixed64,5,opt,name=speedY,proto3" json:"speedY,omitempty"`
	AccelerationX float64                `protobuf:"fixed64,6,opt,name=accelerationX,proto3" json:"accelerationX,omitempty"`
	AccelerationY float64                `protobuf:"fixed64,7,opt,name=accelerationY,proto3" json:"accelerationY,omitempty"`
	unknownFields protoimpl.UnknownFields
	sizeCache     protoimpl.SizeCache
}

func (x *Position) Reset() {
	*x = Position{}
	mi := &file_server_proto_msgTypes[3]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *Position) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*Position) ProtoMessage() {}

func (x *Position) ProtoReflect() protoreflect.Message {
	mi := &file_server_proto_msgTypes[3]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use Position.ProtoReflect.Descriptor instead.
func (*Position) Descriptor() ([]byte, []int) {
	return file_server_proto_rawDescGZIP(), []int{3}
}

func (x *Position) GetX() float64 {
	if x != nil {
		return x.X
	}
	return 0
}

func (x *Position) GetY() float64 {
	if x != nil {
		return x.Y
	}
	return 0
}

func (x *Position) GetAngle() float64 {
	if x != nil {
		return x.Angle
	}
	return 0
}

func (x *Position) GetSpeedX() float64 {
	if x != nil {
		return x.SpeedX
	}
	return 0
}

func (x *Position) GetSpeedY() float64 {
	if x != nil {
		return x.SpeedY
	}
	return 0
}

func (x *Position) GetAccelerationX() float64 {
	if x != nil {
		return x.AccelerationX
	}
	return 0
}

func (x *Position) GetAccelerationY() float64 {
	if x != nil {
		return x.AccelerationY
	}
	return 0
}

type Input struct {
	state         protoimpl.MessageState `protogen:"open.v1"`
	Move          bool                   `protobuf:"varint,1,opt,name=move,proto3" json:"move,omitempty"`
	StrideLeft    bool                   `protobuf:"varint,2,opt,name=stride_left,json=strideLeft,proto3" json:"stride_left,omitempty"`
	StrideRight   bool                   `protobuf:"varint,3,opt,name=stride_right,json=strideRight,proto3" json:"stride_right,omitempty"`
	Stop          bool                   `protobuf:"varint,4,opt,name=stop,proto3" json:"stop,omitempty"`
	IsShoot       bool                   `protobuf:"varint,5,opt,name=is_shoot,json=isShoot,proto3" json:"is_shoot,omitempty"`
	unknownFields protoimpl.UnknownFields
	sizeCache     protoimpl.SizeCache
}

func (x *Input) Reset() {
	*x = Input{}
	mi := &file_server_proto_msgTypes[4]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *Input) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*Input) ProtoMessage() {}

func (x *Input) ProtoReflect() protoreflect.Message {
	mi := &file_server_proto_msgTypes[4]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use Input.ProtoReflect.Descriptor instead.
func (*Input) Descriptor() ([]byte, []int) {
	return file_server_proto_rawDescGZIP(), []int{4}
}

func (x *Input) GetMove() bool {
	if x != nil {
		return x.Move
	}
	return false
}

func (x *Input) GetStrideLeft() bool {
	if x != nil {
		return x.StrideLeft
	}
	return false
}

func (x *Input) GetStrideRight() bool {
	if x != nil {
		return x.StrideRight
	}
	return false
}

func (x *Input) GetStop() bool {
	if x != nil {
		return x.Stop
	}
	return false
}

func (x *Input) GetIsShoot() bool {
	if x != nil {
		return x.IsShoot
	}
	return false
}

type PlayerData struct {
	state         protoimpl.MessageState `protogen:"open.v1"`
	PlayerUuid    string                 `protobuf:"bytes,1,opt,name=player_uuid,json=playerUuid,proto3" json:"player_uuid,omitempty"`
	Timestamp     int64                  `protobuf:"varint,2,opt,name=timestamp,proto3" json:"timestamp,omitempty"` //For sync
	Username      string                 `protobuf:"bytes,3,opt,name=username,proto3" json:"username,omitempty"`
	Color         string                 `protobuf:"bytes,4,opt,name=color,proto3" json:"color,omitempty"`
	Slot          int32                  `protobuf:"varint,5,opt,name=slot,proto3" json:"slot,omitempty"`
	GameCode      string                 `protobuf:"bytes,6,opt,name=game_code,json=gameCode,proto3" json:"game_code,omitempty"` // Código de la partida a la que se une
	Ready         bool                   `protobuf:"varint,7,opt,name=ready,proto3" json:"ready,omitempty"`
	unknownFields protoimpl.UnknownFields
	sizeCache     protoimpl.SizeCache
}

func (x *PlayerData) Reset() {
	*x = PlayerData{}
	mi := &file_server_proto_msgTypes[5]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *PlayerData) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*PlayerData) ProtoMessage() {}

func (x *PlayerData) ProtoReflect() protoreflect.Message {
	mi := &file_server_proto_msgTypes[5]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use PlayerData.ProtoReflect.Descriptor instead.
func (*PlayerData) Descriptor() ([]byte, []int) {
	return file_server_proto_rawDescGZIP(), []int{5}
}

func (x *PlayerData) GetPlayerUuid() string {
	if x != nil {
		return x.PlayerUuid
	}
	return ""
}

func (x *PlayerData) GetTimestamp() int64 {
	if x != nil {
		return x.Timestamp
	}
	return 0
}

func (x *PlayerData) GetUsername() string {
	if x != nil {
		return x.Username
	}
	return ""
}

func (x *PlayerData) GetColor() string {
	if x != nil {
		return x.Color
	}
	return ""
}

func (x *PlayerData) GetSlot() int32 {
	if x != nil {
		return x.Slot
	}
	return 0
}

func (x *PlayerData) GetGameCode() string {
	if x != nil {
		return x.GameCode
	}
	return ""
}

func (x *PlayerData) GetReady() bool {
	if x != nil {
		return x.Ready
	}
	return false
}

type AsteroidState struct {
	state         protoimpl.MessageState `protogen:"open.v1"`
	Id            int32                  `protobuf:"varint,1,opt,name=id,proto3" json:"id,omitempty"`
	X             float64                `protobuf:"fixed64,2,opt,name=x,proto3" json:"x,omitempty"`
	Y             float64                `protobuf:"fixed64,3,opt,name=y,proto3" json:"y,omitempty"`
	Width         int32                  `protobuf:"varint,4,opt,name=width,proto3" json:"width,omitempty"`
	Height        int32                  `protobuf:"varint,5,opt,name=height,proto3" json:"height,omitempty"`
	Speed         float64                `protobuf:"fixed64,6,opt,name=speed,proto3" json:"speed,omitempty"`
	Angle         float64                `protobuf:"fixed64,7,opt,name=angle,proto3" json:"angle,omitempty"`
	Health        int32                  `protobuf:"varint,8,opt,name=health,proto3" json:"health,omitempty"`
	MaxHealth     int32                  `protobuf:"varint,9,opt,name=max_health,json=maxHealth,proto3" json:"max_health,omitempty"`
	unknownFields protoimpl.UnknownFields
	sizeCache     protoimpl.SizeCache
}

func (x *AsteroidState) Reset() {
	*x = AsteroidState{}
	mi := &file_server_proto_msgTypes[6]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *AsteroidState) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*AsteroidState) ProtoMessage() {}

func (x *AsteroidState) ProtoReflect() protoreflect.Message {
	mi := &file_server_proto_msgTypes[6]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use AsteroidState.ProtoReflect.Descriptor instead.
func (*AsteroidState) Descriptor() ([]byte, []int) {
	return file_server_proto_rawDescGZIP(), []int{6}
}

func (x *AsteroidState) GetId() int32 {
	if x != nil {
		return x.Id
	}
	return 0
}

func (x *AsteroidState) GetX() float64 {
	if x != nil {
		return x.X
	}
	return 0
}

func (x *AsteroidState) GetY() float64 {
	if x != nil {
		return x.Y
	}
	return 0
}

func (x *AsteroidState) GetWidth() int32 {
	if x != nil {
		return x.Width
	}
	return 0
}

func (x *AsteroidState) GetHeight() int32 {
	if x != nil {
		return x.Height
	}
	return 0
}

func (x *AsteroidState) GetSpeed() float64 {
	if x != nil {
		return x.Speed
	}
	return 0
}

func (x *AsteroidState) GetAngle() float64 {
	if x != nil {
		return x.Angle
	}
	return 0
}

func (x *AsteroidState) GetHealth() int32 {
	if x != nil {
		return x.Health
	}
	return 0
}

func (x *AsteroidState) GetMaxHealth() int32 {
	if x != nil {
		return x.MaxHealth
	}
	return 0
}

type BulletState struct {
	state         protoimpl.MessageState `protogen:"open.v1"`
	Id            int32                  `protobuf:"varint,1,opt,name=id,proto3" json:"id,omitempty"`
	X             float64                `protobuf:"fixed64,2,opt,name=x,proto3" json:"x,omitempty"`
	Y             float64                `protobuf:"fixed64,3,opt,name=y,proto3" json:"y,omitempty"`
	Angle         float64                `protobuf:"fixed64,4,opt,name=angle,proto3" json:"angle,omitempty"`
	Speed         float64                `protobuf:"fixed64,5,opt,name=speed,proto3" json:"speed,omitempty"`
	Active        bool                   `protobuf:"varint,6,opt,name=active,proto3" json:"active,omitempty"`
	Damage        int32                  `protobuf:"varint,7,opt,name=damage,proto3" json:"damage,omitempty"`
	Width         int32                  `protobuf:"varint,8,opt,name=width,proto3" json:"width,omitempty"`
	Height        int32                  `protobuf:"varint,9,opt,name=height,proto3" json:"height,omitempty"`
	Owneruuid     string                 `protobuf:"bytes,10,opt,name=owneruuid,proto3" json:"owneruuid,omitempty"`
	unknownFields protoimpl.UnknownFields
	sizeCache     protoimpl.SizeCache
}

func (x *BulletState) Reset() {
	*x = BulletState{}
	mi := &file_server_proto_msgTypes[7]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *BulletState) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*BulletState) ProtoMessage() {}

func (x *BulletState) ProtoReflect() protoreflect.Message {
	mi := &file_server_proto_msgTypes[7]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use BulletState.ProtoReflect.Descriptor instead.
func (*BulletState) Descriptor() ([]byte, []int) {
	return file_server_proto_rawDescGZIP(), []int{7}
}

func (x *BulletState) GetId() int32 {
	if x != nil {
		return x.Id
	}
	return 0
}

func (x *BulletState) GetX() float64 {
	if x != nil {
		return x.X
	}
	return 0
}

func (x *BulletState) GetY() float64 {
	if x != nil {
		return x.Y
	}
	return 0
}

func (x *BulletState) GetAngle() float64 {
	if x != nil {
		return x.Angle
	}
	return 0
}

func (x *BulletState) GetSpeed() float64 {
	if x != nil {
		return x.Speed
	}
	return 0
}

func (x *BulletState) GetActive() bool {
	if x != nil {
		return x.Active
	}
	return false
}

func (x *BulletState) GetDamage() int32 {
	if x != nil {
		return x.Damage
	}
	return 0
}

func (x *BulletState) GetWidth() int32 {
	if x != nil {
		return x.Width
	}
	return 0
}

func (x *BulletState) GetHeight() int32 {
	if x != nil {
		return x.Height
	}
	return 0
}

func (x *BulletState) GetOwneruuid() string {
	if x != nil {
		return x.Owneruuid
	}
	return ""
}

type PowerUpState struct {
	state         protoimpl.MessageState `protogen:"open.v1"`
	Id            int32                  `protobuf:"varint,1,opt,name=id,proto3" json:"id,omitempty"`
	X             float64                `protobuf:"fixed64,2,opt,name=x,proto3" json:"x,omitempty"`
	Y             float64                `protobuf:"fixed64,3,opt,name=y,proto3" json:"y,omitempty"`
	Type          string                 `protobuf:"bytes,4,opt,name=type,proto3" json:"type,omitempty"`
	Width         int32                  `protobuf:"varint,5,opt,name=width,proto3" json:"width,omitempty"`
	Height        int32                  `protobuf:"varint,6,opt,name=height,proto3" json:"height,omitempty"`
	Active        bool                   `protobuf:"varint,7,opt,name=active,proto3" json:"active,omitempty"`
	unknownFields protoimpl.UnknownFields
	sizeCache     protoimpl.SizeCache
}

func (x *PowerUpState) Reset() {
	*x = PowerUpState{}
	mi := &file_server_proto_msgTypes[8]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *PowerUpState) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*PowerUpState) ProtoMessage() {}

func (x *PowerUpState) ProtoReflect() protoreflect.Message {
	mi := &file_server_proto_msgTypes[8]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use PowerUpState.ProtoReflect.Descriptor instead.
func (*PowerUpState) Descriptor() ([]byte, []int) {
	return file_server_proto_rawDescGZIP(), []int{8}
}

func (x *PowerUpState) GetId() int32 {
	if x != nil {
		return x.Id
	}
	return 0
}

func (x *PowerUpState) GetX() float64 {
	if x != nil {
		return x.X
	}
	return 0
}

func (x *PowerUpState) GetY() float64 {
	if x != nil {
		return x.Y
	}
	return 0
}

func (x *PowerUpState) GetType() string {
	if x != nil {
		return x.Type
	}
	return ""
}

func (x *PowerUpState) GetWidth() int32 {
	if x != nil {
		return x.Width
	}
	return 0
}

func (x *PowerUpState) GetHeight() int32 {
	if x != nil {
		return x.Height
	}
	return 0
}

func (x *PowerUpState) GetActive() bool {
	if x != nil {
		return x.Active
	}
	return false
}

type LevelState struct {
	state                protoimpl.MessageState `protogen:"open.v1"`
	CurrentLevel         int32                  `protobuf:"varint,1,opt,name=current_level,json=currentLevel,proto3" json:"current_level,omitempty"`
	AsteroidsDestroyed   int32                  `protobuf:"varint,2,opt,name=asteroids_destroyed,json=asteroidsDestroyed,proto3" json:"asteroids_destroyed,omitempty"`
	AsteroidsToNextLevel int32                  `protobuf:"varint,3,opt,name=asteroids_to_next_level,json=asteroidsToNextLevel,proto3" json:"asteroids_to_next_level,omitempty"`
	LevelUpMessageTimer  float64                `protobuf:"fixed64,4,opt,name=level_up_message_timer,json=levelUpMessageTimer,proto3" json:"level_up_message_timer,omitempty"`
	MinAsteroids         int32                  `protobuf:"varint,5,opt,name=min_asteroids,json=minAsteroids,proto3" json:"min_asteroids,omitempty"`
	DifficultyFactor     int32                  `protobuf:"varint,6,opt,name=difficulty_factor,json=difficultyFactor,proto3" json:"difficulty_factor,omitempty"`
	Score                int32                  `protobuf:"varint,7,opt,name=score,proto3" json:"score,omitempty"`
	unknownFields        protoimpl.UnknownFields
	sizeCache            protoimpl.SizeCache
}

func (x *LevelState) Reset() {
	*x = LevelState{}
	mi := &file_server_proto_msgTypes[9]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *LevelState) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*LevelState) ProtoMessage() {}

func (x *LevelState) ProtoReflect() protoreflect.Message {
	mi := &file_server_proto_msgTypes[9]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use LevelState.ProtoReflect.Descriptor instead.
func (*LevelState) Descriptor() ([]byte, []int) {
	return file_server_proto_rawDescGZIP(), []int{9}
}

func (x *LevelState) GetCurrentLevel() int32 {
	if x != nil {
		return x.CurrentLevel
	}
	return 0
}

func (x *LevelState) GetAsteroidsDestroyed() int32 {
	if x != nil {
		return x.AsteroidsDestroyed
	}
	return 0
}

func (x *LevelState) GetAsteroidsToNextLevel() int32 {
	if x != nil {
		return x.AsteroidsToNextLevel
	}
	return 0
}

func (x *LevelState) GetLevelUpMessageTimer() float64 {
	if x != nil {
		return x.LevelUpMessageTimer
	}
	return 0
}

func (x *LevelState) GetMinAsteroids() int32 {
	if x != nil {
		return x.MinAsteroids
	}
	return 0
}

func (x *LevelState) GetDifficultyFactor() int32 {
	if x != nil {
		return x.DifficultyFactor
	}
	return 0
}

func (x *LevelState) GetScore() int32 {
	if x != nil {
		return x.Score
	}
	return 0
}

type GameState struct {
	state         protoimpl.MessageState  `protogen:"open.v1"`
	PlayerStates  map[string]*PlayerState `protobuf:"bytes,1,rep,name=playerStates,proto3" json:"playerStates,omitempty" protobuf_key:"bytes,1,opt,name=key" protobuf_val:"bytes,2,opt,name=value"`
	Asteroids     []*AsteroidState        `protobuf:"bytes,2,rep,name=asteroids,proto3" json:"asteroids,omitempty"`
	Bullets       []*BulletState          `protobuf:"bytes,3,rep,name=bullets,proto3" json:"bullets,omitempty"`
	Powerups      []*PowerUpState         `protobuf:"bytes,4,rep,name=powerups,proto3" json:"powerups,omitempty"`
	Level         *LevelState             `protobuf:"bytes,5,opt,name=level,proto3" json:"level,omitempty"`
	unknownFields protoimpl.UnknownFields
	sizeCache     protoimpl.SizeCache
}

func (x *GameState) Reset() {
	*x = GameState{}
	mi := &file_server_proto_msgTypes[10]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *GameState) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*GameState) ProtoMessage() {}

func (x *GameState) ProtoReflect() protoreflect.Message {
	mi := &file_server_proto_msgTypes[10]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use GameState.ProtoReflect.Descriptor instead.
func (*GameState) Descriptor() ([]byte, []int) {
	return file_server_proto_rawDescGZIP(), []int{10}
}

func (x *GameState) GetPlayerStates() map[string]*PlayerState {
	if x != nil {
		return x.PlayerStates
	}
	return nil
}

func (x *GameState) GetAsteroids() []*AsteroidState {
	if x != nil {
		return x.Asteroids
	}
	return nil
}

func (x *GameState) GetBullets() []*BulletState {
	if x != nil {
		return x.Bullets
	}
	return nil
}

func (x *GameState) GetPowerups() []*PowerUpState {
	if x != nil {
		return x.Powerups
	}
	return nil
}

func (x *GameState) GetLevel() *LevelState {
	if x != nil {
		return x.Level
	}
	return nil
}

type GameData struct {
	state         protoimpl.MessageState `protogen:"open.v1"`
	Code          string                 `protobuf:"bytes,1,opt,name=code,proto3" json:"code,omitempty"`       // Unique game code
	Players       []*PlayerData          `protobuf:"bytes,2,rep,name=players,proto3" json:"players,omitempty"` // List of players in the game
	Started       bool                   `protobuf:"varint,4,opt,name=started,proto3" json:"started,omitempty"`
	unknownFields protoimpl.UnknownFields
	sizeCache     protoimpl.SizeCache
}

func (x *GameData) Reset() {
	*x = GameData{}
	mi := &file_server_proto_msgTypes[11]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *GameData) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*GameData) ProtoMessage() {}

func (x *GameData) ProtoReflect() protoreflect.Message {
	mi := &file_server_proto_msgTypes[11]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use GameData.ProtoReflect.Descriptor instead.
func (*GameData) Descriptor() ([]byte, []int) {
	return file_server_proto_rawDescGZIP(), []int{11}
}

func (x *GameData) GetCode() string {
	if x != nil {
		return x.Code
	}
	return ""
}

func (x *GameData) GetPlayers() []*PlayerData {
	if x != nil {
		return x.Players
	}
	return nil
}

func (x *GameData) GetStarted() bool {
	if x != nil {
		return x.Started
	}
	return false
}

type Empty struct {
	state         protoimpl.MessageState `protogen:"open.v1"`
	unknownFields protoimpl.UnknownFields
	sizeCache     protoimpl.SizeCache
}

func (x *Empty) Reset() {
	*x = Empty{}
	mi := &file_server_proto_msgTypes[12]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *Empty) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*Empty) ProtoMessage() {}

func (x *Empty) ProtoReflect() protoreflect.Message {
	mi := &file_server_proto_msgTypes[12]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use Empty.ProtoReflect.Descriptor instead.
func (*Empty) Descriptor() ([]byte, []int) {
	return file_server_proto_rawDescGZIP(), []int{12}
}

var File_server_proto protoreflect.FileDescriptor

const file_server_proto_rawDesc = "" +
	"\n" +
	"\fserver.proto\x12\x06server\"#\n" +
	"\vBoolMessage\x12\x14\n" +
	"\x05value\x18\x01 \x01(\bR\x05value\"\x1e\n" +
	"\bGameCode\x12\x12\n" +
	"\x04code\x18\x01 \x01(\tR\x04code\"\xcb\x01\n" +
	"\vPlayerState\x12\x12\n" +
	"\x04code\x18\x01 \x01(\tR\x04code\x12\x1f\n" +
	"\vplayer_uuid\x18\x02 \x01(\tR\n" +
	"playerUuid\x12\x1c\n" +
	"\ttimestamp\x18\x03 \x01(\x03R\ttimestamp\x12#\n" +
	"\x05input\x18\x05 \x01(\v2\r.server.InputR\x05input\x12,\n" +
	"\bposition\x18\x06 \x01(\v2\x10.server.PositionR\bposition\x12\x16\n" +
	"\x06health\x18\a \x01(\x05R\x06health\"\xb8\x01\n" +
	"\bPosition\x12\f\n" +
	"\x01x\x18\x01 \x01(\x01R\x01x\x12\f\n" +
	"\x01y\x18\x02 \x01(\x01R\x01y\x12\x14\n" +
	"\x05angle\x18\x03 \x01(\x01R\x05angle\x12\x16\n" +
	"\x06speedX\x18\x04 \x01(\x01R\x06speedX\x12\x16\n" +
	"\x06speedY\x18\x05 \x01(\x01R\x06speedY\x12$\n" +
	"\raccelerationX\x18\x06 \x01(\x01R\raccelerationX\x12$\n" +
	"\raccelerationY\x18\a \x01(\x01R\raccelerationY\"\x8e\x01\n" +
	"\x05Input\x12\x12\n" +
	"\x04move\x18\x01 \x01(\bR\x04move\x12\x1f\n" +
	"\vstride_left\x18\x02 \x01(\bR\n" +
	"strideLeft\x12!\n" +
	"\fstride_right\x18\x03 \x01(\bR\vstrideRight\x12\x12\n" +
	"\x04stop\x18\x04 \x01(\bR\x04stop\x12\x19\n" +
	"\bis_shoot\x18\x05 \x01(\bR\aisShoot\"\xc4\x01\n" +
	"\n" +
	"PlayerData\x12\x1f\n" +
	"\vplayer_uuid\x18\x01 \x01(\tR\n" +
	"playerUuid\x12\x1c\n" +
	"\ttimestamp\x18\x02 \x01(\x03R\ttimestamp\x12\x1a\n" +
	"\busername\x18\x03 \x01(\tR\busername\x12\x14\n" +
	"\x05color\x18\x04 \x01(\tR\x05color\x12\x12\n" +
	"\x04slot\x18\x05 \x01(\x05R\x04slot\x12\x1b\n" +
	"\tgame_code\x18\x06 \x01(\tR\bgameCode\x12\x14\n" +
	"\x05ready\x18\a \x01(\bR\x05ready\"\xcc\x01\n" +
	"\rAsteroidState\x12\x0e\n" +
	"\x02id\x18\x01 \x01(\x05R\x02id\x12\f\n" +
	"\x01x\x18\x02 \x01(\x01R\x01x\x12\f\n" +
	"\x01y\x18\x03 \x01(\x01R\x01y\x12\x14\n" +
	"\x05width\x18\x04 \x01(\x05R\x05width\x12\x16\n" +
	"\x06height\x18\x05 \x01(\x05R\x06height\x12\x14\n" +
	"\x05speed\x18\x06 \x01(\x01R\x05speed\x12\x14\n" +
	"\x05angle\x18\a \x01(\x01R\x05angle\x12\x16\n" +
	"\x06health\x18\b \x01(\x05R\x06health\x12\x1d\n" +
	"\n" +
	"max_health\x18\t \x01(\x05R\tmaxHealth\"\xe1\x01\n" +
	"\vBulletState\x12\x0e\n" +
	"\x02id\x18\x01 \x01(\x05R\x02id\x12\f\n" +
	"\x01x\x18\x02 \x01(\x01R\x01x\x12\f\n" +
	"\x01y\x18\x03 \x01(\x01R\x01y\x12\x14\n" +
	"\x05angle\x18\x04 \x01(\x01R\x05angle\x12\x14\n" +
	"\x05speed\x18\x05 \x01(\x01R\x05speed\x12\x16\n" +
	"\x06active\x18\x06 \x01(\bR\x06active\x12\x16\n" +
	"\x06damage\x18\a \x01(\x05R\x06damage\x12\x14\n" +
	"\x05width\x18\b \x01(\x05R\x05width\x12\x16\n" +
	"\x06height\x18\t \x01(\x05R\x06height\x12\x1c\n" +
	"\towneruuid\x18\n" +
	" \x01(\tR\towneruuid\"\x94\x01\n" +
	"\fPowerUpState\x12\x0e\n" +
	"\x02id\x18\x01 \x01(\x05R\x02id\x12\f\n" +
	"\x01x\x18\x02 \x01(\x01R\x01x\x12\f\n" +
	"\x01y\x18\x03 \x01(\x01R\x01y\x12\x12\n" +
	"\x04type\x18\x04 \x01(\tR\x04type\x12\x14\n" +
	"\x05width\x18\x05 \x01(\x05R\x05width\x12\x16\n" +
	"\x06height\x18\x06 \x01(\x05R\x06height\x12\x16\n" +
	"\x06active\x18\a \x01(\bR\x06active\"\xb6\x02\n" +
	"\n" +
	"LevelState\x12#\n" +
	"\rcurrent_level\x18\x01 \x01(\x05R\fcurrentLevel\x12/\n" +
	"\x13asteroids_destroyed\x18\x02 \x01(\x05R\x12asteroidsDestroyed\x125\n" +
	"\x17asteroids_to_next_level\x18\x03 \x01(\x05R\x14asteroidsToNextLevel\x123\n" +
	"\x16level_up_message_timer\x18\x04 \x01(\x01R\x13levelUpMessageTimer\x12#\n" +
	"\rmin_asteroids\x18\x05 \x01(\x05R\fminAsteroids\x12+\n" +
	"\x11difficulty_factor\x18\x06 \x01(\x05R\x10difficultyFactor\x12\x14\n" +
	"\x05score\x18\a \x01(\x05R\x05score\"\xea\x02\n" +
	"\tGameState\x12G\n" +
	"\fplayerStates\x18\x01 \x03(\v2#.server.GameState.PlayerStatesEntryR\fplayerStates\x123\n" +
	"\tasteroids\x18\x02 \x03(\v2\x15.server.AsteroidStateR\tasteroids\x12-\n" +
	"\abullets\x18\x03 \x03(\v2\x13.server.BulletStateR\abullets\x120\n" +
	"\bpowerups\x18\x04 \x03(\v2\x14.server.PowerUpStateR\bpowerups\x12(\n" +
	"\x05level\x18\x05 \x01(\v2\x12.server.LevelStateR\x05level\x1aT\n" +
	"\x11PlayerStatesEntry\x12\x10\n" +
	"\x03key\x18\x01 \x01(\tR\x03key\x12)\n" +
	"\x05value\x18\x02 \x01(\v2\x13.server.PlayerStateR\x05value:\x028\x01\"f\n" +
	"\bGameData\x12\x12\n" +
	"\x04code\x18\x01 \x01(\tR\x04code\x12,\n" +
	"\aplayers\x18\x02 \x03(\v2\x12.server.PlayerDataR\aplayers\x12\x18\n" +
	"\astarted\x18\x04 \x01(\bR\astarted\"\a\n" +
	"\x05Empty2\xe4\x01\n" +
	"\vGameService\x12-\n" +
	"\n" +
	"CreateGame\x12\r.server.Empty\x1a\x10.server.GameCode\x122\n" +
	"\bJoinGame\x12\x12.server.PlayerData\x1a\x10.server.GameData0\x01\x12>\n" +
	"\x10JoinInputUpdates\x12\x13.server.PlayerState\x1a\x11.server.GameState(\x010\x01\x122\n" +
	"\tStartGame\x12\x10.server.GameCode\x1a\x13.server.BoolMessageB\x0fZ\rTrashed/protob\x06proto3"

var (
	file_server_proto_rawDescOnce sync.Once
	file_server_proto_rawDescData []byte
)

func file_server_proto_rawDescGZIP() []byte {
	file_server_proto_rawDescOnce.Do(func() {
		file_server_proto_rawDescData = protoimpl.X.CompressGZIP(unsafe.Slice(unsafe.StringData(file_server_proto_rawDesc), len(file_server_proto_rawDesc)))
	})
	return file_server_proto_rawDescData
}

var file_server_proto_msgTypes = make([]protoimpl.MessageInfo, 14)
var file_server_proto_goTypes = []any{
	(*BoolMessage)(nil),   // 0: server.BoolMessage
	(*GameCode)(nil),      // 1: server.GameCode
	(*PlayerState)(nil),   // 2: server.PlayerState
	(*Position)(nil),      // 3: server.Position
	(*Input)(nil),         // 4: server.Input
	(*PlayerData)(nil),    // 5: server.PlayerData
	(*AsteroidState)(nil), // 6: server.AsteroidState
	(*BulletState)(nil),   // 7: server.BulletState
	(*PowerUpState)(nil),  // 8: server.PowerUpState
	(*LevelState)(nil),    // 9: server.LevelState
	(*GameState)(nil),     // 10: server.GameState
	(*GameData)(nil),      // 11: server.GameData
	(*Empty)(nil),         // 12: server.Empty
	nil,                   // 13: server.GameState.PlayerStatesEntry
}
var file_server_proto_depIdxs = []int32{
	4,  // 0: server.PlayerState.input:type_name -> server.Input
	3,  // 1: server.PlayerState.position:type_name -> server.Position
	13, // 2: server.GameState.playerStates:type_name -> server.GameState.PlayerStatesEntry
	6,  // 3: server.GameState.asteroids:type_name -> server.AsteroidState
	7,  // 4: server.GameState.bullets:type_name -> server.BulletState
	8,  // 5: server.GameState.powerups:type_name -> server.PowerUpState
	9,  // 6: server.GameState.level:type_name -> server.LevelState
	5,  // 7: server.GameData.players:type_name -> server.PlayerData
	2,  // 8: server.GameState.PlayerStatesEntry.value:type_name -> server.PlayerState
	12, // 9: server.GameService.CreateGame:input_type -> server.Empty
	5,  // 10: server.GameService.JoinGame:input_type -> server.PlayerData
	2,  // 11: server.GameService.JoinInputUpdates:input_type -> server.PlayerState
	1,  // 12: server.GameService.StartGame:input_type -> server.GameCode
	1,  // 13: server.GameService.CreateGame:output_type -> server.GameCode
	11, // 14: server.GameService.JoinGame:output_type -> server.GameData
	10, // 15: server.GameService.JoinInputUpdates:output_type -> server.GameState
	0,  // 16: server.GameService.StartGame:output_type -> server.BoolMessage
	13, // [13:17] is the sub-list for method output_type
	9,  // [9:13] is the sub-list for method input_type
	9,  // [9:9] is the sub-list for extension type_name
	9,  // [9:9] is the sub-list for extension extendee
	0,  // [0:9] is the sub-list for field type_name
}

func init() { file_server_proto_init() }
func file_server_proto_init() {
	if File_server_proto != nil {
		return
	}
	type x struct{}
	out := protoimpl.TypeBuilder{
		File: protoimpl.DescBuilder{
			GoPackagePath: reflect.TypeOf(x{}).PkgPath(),
			RawDescriptor: unsafe.Slice(unsafe.StringData(file_server_proto_rawDesc), len(file_server_proto_rawDesc)),
			NumEnums:      0,
			NumMessages:   14,
			NumExtensions: 0,
			NumServices:   1,
		},
		GoTypes:           file_server_proto_goTypes,
		DependencyIndexes: file_server_proto_depIdxs,
		MessageInfos:      file_server_proto_msgTypes,
	}.Build()
	File_server_proto = out.File
	file_server_proto_goTypes = nil
	file_server_proto_depIdxs = nil
}
