export interface Item {
  item_id: string;
  market_hash_name: string;
  type: string;
  url: string;
}

export interface PriceData {
  price: number;
  timestamp: string;
  source: string;
}