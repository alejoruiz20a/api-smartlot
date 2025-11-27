from app import db
from datetime import datetime
import enum
from werkzeug.security import generate_password_hash, check_password_hash

# =========================
# ENUMS
# =========================
class VehicleType(enum.Enum):
    car = 'car'
    motorcycle = 'motorcycle'
    bicycle = 'bicycle'
    truck = 'truck'
    other = 'other'

class RegistrationState(enum.Enum):
    active = 'active'
    exited = 'exited'
    cancelled = 'cancelled'

class InvoiceState(enum.Enum):
    pending = 'pending'
    paid = 'paid'
    void = 'void'

class PaymentMethod(enum.Enum):
    cash = 'cash'
    card = 'card'
    mobile = 'mobile'
    transfer = 'transfer'
    other = 'other'

# =========================
# Usuarios y Roles
# =========================
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    
    user_roles = db.relationship('UserRole', back_populates='user', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Genera el hash de la contraseña"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica la contraseña contra el hash almacenado"""
        return check_password_hash(self.password_hash, password)

class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    
    user_roles = db.relationship('UserRole', back_populates='role', cascade='all, delete-orphan')

class UserRole(db.Model):
    __tablename__ = 'user_roles'
    
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    role_id = db.Column(db.BigInteger, db.ForeignKey('roles.id', ondelete='CASCADE'), nullable=False)
    
    user = db.relationship('User', back_populates='user_roles')
    role = db.relationship('Role', back_populates='user_roles')

# =========================
# Parqueaderos
# =========================
class Parking(db.Model):
    __tablename__ = 'parkings'
    
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.Text)
    capacity_estimated = db.Column(db.Integer)
    enabled = db.Column(db.Boolean, default=True)
    
    zones = db.relationship('ParkingZone', back_populates='parking', cascade='all, delete-orphan')
    cells = db.relationship('Cell', back_populates='parking', cascade='all, delete-orphan')
    registrations = db.relationship('Registration', back_populates='parking', cascade='all, delete-orphan')
    invoices = db.relationship('Invoice', back_populates='parking', cascade='all, delete-orphan')

class ParkingZone(db.Model):
    __tablename__ = 'parking_zones'
    
    id = db.Column(db.BigInteger, primary_key=True)
    parking_id = db.Column(db.BigInteger, db.ForeignKey('parkings.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(120))
    level = db.Column(db.Integer)
    
    parking = db.relationship('Parking', back_populates='zones')
    cells = db.relationship('Cell', back_populates='zone')

class Cell(db.Model):
    __tablename__ = 'cells'
    
    id = db.Column(db.BigInteger, primary_key=True)
    parking_id = db.Column(db.BigInteger, db.ForeignKey('parkings.id', ondelete='CASCADE'), nullable=False)
    zone_id = db.Column(db.BigInteger, db.ForeignKey('parking_zones.id', ondelete='SET NULL'))
    code = db.Column(db.String(50), nullable=False)
    vehicle_type = db.Column(db.Enum(VehicleType), default=VehicleType.car)
    status = db.Column(db.String(30), default='available')
    
    _table_args_ = (
        db.UniqueConstraint('parking_id', 'code', name='uq_parking_code'),
    )
    
    parking = db.relationship('Parking', back_populates='cells')
    zone = db.relationship('ParkingZone', back_populates='cells')
    registrations = db.relationship('Registration', back_populates='cell')

# =========================
# Vehículos
# =========================
class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    
    id = db.Column(db.BigInteger, primary_key=True)
    plate = db.Column(db.String(30), unique=True, nullable=False)
    type = db.Column(db.Enum(VehicleType), default=VehicleType.car)
    
    registrations = db.relationship('Registration', back_populates='vehicle')

# =========================
# Registros de entrada/salida
# =========================
class Registration(db.Model):
    __tablename__ = 'registrations'
    
    id = db.Column(db.BigInteger, primary_key=True)
    parking_id = db.Column(db.BigInteger, db.ForeignKey('parkings.id', ondelete='CASCADE'), nullable=False)
    cell_id = db.Column(db.BigInteger, db.ForeignKey('cells.id', ondelete='SET NULL'))
    vehicle_id = db.Column(db.BigInteger, db.ForeignKey('vehicles.id', ondelete='SET NULL'))
    state = db.Column(db.Enum(RegistrationState), default=RegistrationState.active)
    checkin_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    checkout_at = db.Column(db.DateTime(timezone=True))
    
    parking = db.relationship('Parking', back_populates='registrations')
    cell = db.relationship('Cell', back_populates='registrations')
    vehicle = db.relationship('Vehicle', back_populates='registrations')
    invoices = db.relationship('Invoice', back_populates='registration')

# =========================
# Facturación y Pagos
# =========================
class Invoice(db.Model):
    __tablename__ = 'invoices'
    
    id = db.Column(db.BigInteger, primary_key=True)
    registration_id = db.Column(db.BigInteger, db.ForeignKey('registrations.id', ondelete='SET NULL'))
    parking_id = db.Column(db.BigInteger, db.ForeignKey('parkings.id', ondelete='CASCADE'), nullable=False)
    total = db.Column(db.Numeric(12, 2), default=0)
    state = db.Column(db.Enum(InvoiceState), default=InvoiceState.pending)
    issued_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    
    registration = db.relationship('Registration', back_populates='invoices')
    parking = db.relationship('Parking', back_populates='invoices')
    payments = db.relationship('Payment', back_populates='invoice', cascade='all, delete-orphan')

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.BigInteger, primary_key=True)
    invoice_id = db.Column(db.BigInteger, db.ForeignKey('invoices.id', ondelete='CASCADE'), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    method = db.Column(db.Enum(PaymentMethod), default=PaymentMethod.cash)
    paid_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    
    invoice = db.relationship('Invoice', back_populates='payments')