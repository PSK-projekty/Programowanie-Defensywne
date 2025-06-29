
# vetclinic_gui/services/blockchain_service.py
import json
from datetime import datetime
from typing import Dict, List, Optional

from web3 import Web3
from web3.contract import Contract

from vetclinic_gui.services.config import settings


class BlockchainService:
    """
    Serwis do komunikacji ze smart kontraktem MedicalRecord na blockchainie.
    Zapewnia odczyt historii medycznej i operacje CRUD na rekordach.
    """

    def __init__(
        self,
        provider_url: Optional[str] = None,
        contract_address: Optional[str] = None,
        abi_path: Optional[str] = None
    ):
        # Ustawienia: można podać ręcznie lub brać z settings
        self.provider_url = provider_url or settings.BLOCKCHAIN_URL
        self.contract_address = contract_address or settings.CONTRACT_ADDRESS
        self.abi_path = abi_path or settings.CONTRACT_ABI_PATH

        # Init Web3
        self.w3: Web3 = Web3(Web3.HTTPProvider(self.provider_url))
        self.connected: bool = self.w3.is_connected()
        if not self.connected:
            print(f"🚨 Ostrzeżenie: nie można połączyć się z nodem blockchain pod {self.provider_url}")

        # Wczytanie ABI i inicjalizacja kontraktu
        self.contract: Optional[Contract] = None
        if self.abi_path and self.contract_address:
            try:
                with open(self.abi_path, 'r', encoding='utf-8') as f:
                    abi = json.load(f)
                address = Web3.to_checksum_address(self.contract_address)
                self.contract = self.w3.eth.contract(address=address, abi=abi)
                print(f"✅ Kontrakt wczytany: {address}")
            except FileNotFoundError:
                print(f"🚨 Plik ABI nie znaleziony: {self.abi_path}")
            except Exception as e:
                print(f"🚨 Błąd inicjalizacji kontraktu: {e}")
        else:
            print("⚠️  Brak ustawień kontraktu (address/ABI) — nie będzie można wykonywać operacji na blockchainie.")

    def ensure_connection(self):
        if not self.connected:
            raise ConnectionError(f"Brak połączenia z blockchainem ({self.provider_url}).")

    def ensure_contract(self):
        if not self.contract:
            raise RuntimeError("Kontrakt nie został poprawnie zainicjalizowany.")

    def get_medical_history(self, owner_address: str) -> List[Dict]:
        """
        Pobiera wszystkie rekordy medyczne dla danego właściciela.
        Zwraca listę dict z kluczami:
        id, data_hash, date, deleted, owner, tx_hash
        """
        self.ensure_connection()
        self.ensure_contract()
        checksum = Web3.to_checksum_address(owner_address)

        try:
            ids: List[int] = self.contract.functions.getRecordsByOwner(checksum).call()
        except Exception as e:
            raise RuntimeError(f"Błąd przy pobieraniu ID rekordów: {e}")

        history: List[Dict] = []
        for rec_id in ids:
            try:
                tup = self.contract.functions.getRecord(rec_id).call()
            except Exception:
                continue

            rec = {
                'id': tup[0],
                'data_hash': tup[1],
                'date': datetime.fromtimestamp(tup[2]),
                'deleted': tup[3],
                'owner': tup[4],
                'tx_hash': None
            }
            history.append(rec)

        history.sort(key=lambda x: x['date'])
        return history

    def add_record(
        self,
        rec_id: int,
        data_hash: str,
        from_address: str,
        private_key: str
    ) -> str:
        """
        Wysyła transakcję addRecord. Zwraca tx_hash.
        """
        self.ensure_connection()
        self.ensure_contract()
        checksum = Web3.to_checksum_address(from_address)
        nonce = self.w3.eth.get_transaction_count(checksum)
        tx = self.contract.functions.addRecord(rec_id, data_hash).build_transaction({
            'from': checksum,
            'nonce': nonce,
            'gas': 200000,
            'gasPrice': self.w3.to_wei('5', 'gwei')
        })
        signed = self.w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
        return tx_hash.hex()

    def update_record(
        self,
        rec_id: int,
        new_data_hash: str,
        from_address: str,
        private_key: str
    ) -> str:
        """
        Wysyła transakcję updateRecord. Zwraca tx_hash.
        """
        self.ensure_connection()
        self.ensure_contract()
        checksum = Web3.to_checksum_address(from_address)
        nonce = self.w3.eth.get_transaction_count(checksum)
        tx = self.contract.functions.updateRecord(rec_id, new_data_hash).build_transaction({
            'from': checksum,
            'nonce': nonce,
            'gas': 200000,
            'gasPrice': self.w3.to_wei('5', 'gwei')
        })
        signed = self.w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
        return tx_hash.hex()

    def delete_record(
        self,
        rec_id: int,
        from_address: str,
        private_key: str
    ) -> str:
        """
        Wysyła transakcję deleteRecord. Zwraca tx_hash.
        """
        self.ensure_connection()
        self.ensure_contract()
        checksum = Web3.to_checksum_address(from_address)
        nonce = self.w3.eth.get_transaction_count(checksum)
        tx = self.contract.functions.deleteRecord(rec_id).build_transaction({
            'from': checksum,
            'nonce': nonce,
            'gas': 200000,
            'gasPrice': self.w3.to_wei('5', 'gwei')
        })
        signed = self.w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
        return tx_hash.hex()