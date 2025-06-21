#!/usr/bin/env python3
"""
检查数据库中的赛道数据
"""

from app.core.database import get_db
from app.models import Circuit

def main():
    db = next(get_db())
    
    try:
        circuits = db.query(Circuit).order_by(Circuit.circuit_name).all()
        
        print(f'数据库中的赛道 (共{len(circuits)}个):')
        print('=' * 80)
        
        for circuit in circuits:
            print(f'{circuit.circuit_name} ({circuit.country}) - {circuit.locality}')
            
    finally:
        db.close()

if __name__ == "__main__":
    main() 