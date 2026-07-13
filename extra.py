

#3 - DML
db = SessionLocal()

if db.query(HeavyEquipment).count() == 0:
    print("\n--- Inserting new Data ---")

# Parents
    excavator = HeavyEquipment(machine_name="CAT-320", machine_type="Excavator")
    bulldozer = HeavyEquipment(machine_name="Komatsu-D39", machine_type="Bulldozer")
    new_crane = HeavyEquipment(machine_name="Liebherr-LTM", machine_type="Crane")

# Children
    log_1 = MaintenanceLog(description="Replaced hydraulic hose", cost=1500.00, machine=excavator)
    log_2 = MaintenanceLog(description="Routine oil change", cost=450.00, machine=excavator)
    log_3 = MaintenanceLog(description="Routine oil change", cost=450.00, machine=excavator)

# M:N mechanics entities
    mutu = Mechanic(name="Mutu")
    ah_chong = Mechanic(name="Ah Chong")

    excavator.mechanics.extend([mutu, ah_chong]) #both work on it
    bulldozer.mechanics.append(mutu) #only mutu

    db.add_all([excavator, bulldozer, new_crane, log_1, log_2, log_3, mutu, ah_chong])
    db.commit()
    print("Data uploaded to PostgreSQL")


# #Printing on the terminal
# print(f"\n{'Machine':<15} | {'Maintenance Issue' :<25} | {'Cost'}")
# print("-" * 55)

# for machine_name, description, cost in results:
#     print(f"{machine_name:<15} | {description:<25} | RM {cost}")


# #LEFT JOIN
# results = db.query(
#     HeavyEquipment.machine_name,
#     MaintenanceLog.description,
# ).outerjoin(MaintenanceLog).all()

# print(f"\n{'MACHINE':<15} | {'MAINTENANCE ISSUE'}")
# print("-" * 40)

# for machine_name, description in results:
#     display_desc = description if description else "NO LOGS (BRAND NEW)"
#     print(f"{machine_name:<15} | {display_desc}")


# #5 - IS NULL

# missing_logs = db.query(
#     HeavyEquipment.machine_name
# ).outerjoin(MaintenanceLog).filter(
#     MaintenanceLog.log_id.is_(None)
# ).all()

# print("Machines with ZERO maintenance logs:")
# for machine in missing_logs:
#     print(f"- {machine[0]}")

# db.close()

# # cursor.execute("SELECT hero, kills, deaths FROM match_stats WHERE player_id = 99 AND kills >15")
# # results = cursor.fetchall()



# # high_kill_games = session.query(MatchState).filter(MatchStat.player_id == 99, MatchStat.kills >15).all()

# # for game in high_kill_games:
# #     print(f"Hero: {game.hero}, Kills: {game.kills}")

from sqlalchemy import Boolean, Column, DateTime, String

class HeavyEquipment(Base):
    __tablename__ = 'heavy_equipment'
    equipment_id = Column(Integer, primary_key=True)
    machine_name = Column(String(100), nullable=False)
    machine_type = Column(String(50))
    is_active = Column(Boolean, default=True)  # Soft delete/flag technique
    #deleted_at = Column(DateTime, nullable=True) #YYYY-MM-DD HH:MM:SS #Soft delete/flag technique
    # if the column is NULL, the machine is active

# 1. Find the machine
excavator = db.query(HeavyEquipment).filter(HeavyEquipment.machine_name == "CAT-320").first()

# 2. Flip the flag (soft delete)
excavator.is_active = False

# 3. Save
db.commit()
print("this machine is retired")

# Only pull machine that are currently active. since we still have the physical data in database
active_machines = db.query(HeavyEquipment).filter(HeavyEquipment.is_active == True).all()

for machine in active_machines:
    print(machine.machine_name)


import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey, Table, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

load_dotenv()

db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_host = os.getenv("DB_HOST")
db.post = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql+psychopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

