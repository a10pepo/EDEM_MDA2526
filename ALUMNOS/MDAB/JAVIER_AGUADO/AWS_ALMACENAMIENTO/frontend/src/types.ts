export interface Airplane {
  plate_number: string;
  type: string;
  last_maintenance_date: string;
  next_maintenance_date: string;
  capacity: number;
  owner_id: string;
  owner_name: string;
  hangar_id: string;
  fuel_capacity: number;
  days_until_maintenance: number;
  maintenance_alert: boolean;
}

export interface AirplaneCreate {
  plate_number: string;
  type: string;
  last_maintenance_date: string;
  next_maintenance_date: string;
  capacity: number;
  owner_id: string;
  owner_name: string;
  hangar_id: string;
  fuel_capacity: number;
}

export interface PassengerInfo {
  passenger_id: string;
  status: string;
}

export interface Flight {
  flight_id: string;
  plate_number: string;
  arrival_time: string;
  departure_time: string;
  fuel_consumption: number;
  occupied_seats: number;
  origin: string;
  destination: string;
  passengers: PassengerInfo[];
  empty_seats: number;
  empty_seats_alert: boolean;
  fuel_alert: boolean;
}

export interface FlightCreate {
  flight_id: string;
  plate_number: string;
  arrival_time: string;
  departure_time: string;
  fuel_consumption: number;
  occupied_seats: number;
  origin: string;
  destination: string;
  passengers: PassengerInfo[];
}

export interface Passenger {
  passenger_id: string;
  name: string;
  national_id: string;
  date_of_birth: string;
}

export interface PassengerCreate {
  passenger_id: string;
  name: string;
  national_id: string;
  date_of_birth: string;
}
