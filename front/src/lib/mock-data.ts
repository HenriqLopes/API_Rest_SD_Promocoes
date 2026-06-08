import tv from "@/assets/product-tv.jpg";
import keyboard from "@/assets/product-keyboard.jpg";
import headphones from "@/assets/product-headphones.jpg";
import airfryer from "@/assets/product-airfryer.jpg";
import phone from "@/assets/product-phone.jpg";
import coffee from "@/assets/product-coffee.jpg";
import controller from "@/assets/product-controller.jpg";
import shoes from "@/assets/product-shoes.jpg";

export const HOT_DEAL_THRESHOLD = 100;

export type Category =
  | "Eletrônicos"
  | "Hardware"
  | "Games"
  | "Smartphones"
  | "Casa e Cozinha"
  | "Áudio"
  | "Moda";

export const CATEGORIES: { name: Category; emoji: string }[] = [
  { name: "Eletrônicos", emoji: "📺" },
  { name: "Hardware", emoji: "💻" },
  { name: "Games", emoji: "🎮" },
  { name: "Smartphones", emoji: "📱" },
  { name: "Casa e Cozinha", emoji: "🏠" },
  { name: "Áudio", emoji: "🔊" },
  { name: "Moda", emoji: "👟" },
];

export type Promotion = {
  id: string;
  title: string;
  store: string;
  category: Category;
  image: string;
  price: number;
  originalPrice: number;
  votes: number;
};

export const PROMOTIONS: Promotion[] = [
  { id: "8432", title: 'Smart TV 55" Crystal UHD 4K Samsung BU8000', store: "Amazon", category: "Eletrônicos", image: tv, price: 2450, originalPrice: 3499, votes: 142 },
  { id: "1294", title: "Teclado Mecânico Logitech G915 TKL RGB Wireless", store: "Kabum", category: "Hardware", image: keyboard, price: 899, originalPrice: 1200, votes: 45 },
  { id: "5521", title: "Fone de Ouvido Bluetooth Sony WH-1000XM5", store: "Mercado Livre", category: "Áudio", image: headphones, price: 1950, originalPrice: 2400, votes: 218 },
  { id: "9901", title: "Air Fryer Mondial Family 4L Inox - Preto/Prata", store: "Magalu", category: "Casa e Cozinha", image: airfryer, price: 329.9, originalPrice: 499, votes: 210 },
  { id: "7710", title: "Smartphone Galaxy S24 256GB Azul Cobalto", store: "Amazon", category: "Smartphones", image: phone, price: 3799, originalPrice: 4999, votes: 87 },
  { id: "6655", title: "Cafeteira Espresso Nespresso Vertuo Pop Preta", store: "Magalu", category: "Casa e Cozinha", image: coffee, price: 499, originalPrice: 799, votes: 31 },
  { id: "3344", title: "Controle Xbox Wireless Robot White Series X|S", store: "Kabum", category: "Games", image: controller, price: 379, originalPrice: 499, votes: 156 },
  { id: "2211", title: "Tênis Esportivo Running Pro Cushion Laranja", store: "Netshoes", category: "Moda", image: shoes, price: 299.9, originalPrice: 549, votes: 64 },
  { id: "4040", title: "Monitor Ultrawide 34” 144Hz QHD HDR400", store: "Kabum", category: "Hardware", image: tv, price: 2899, originalPrice: 3899, votes: 109 },
  { id: "5151", title: "iPhone 15 Pro 256GB Titânio Natural", store: "Apple Store", category: "Smartphones", image: phone, price: 8999, originalPrice: 10499, votes: 320 },
  { id: "6262", title: "Soundbar 5.1 Dolby Atmos com Subwoofer Wireless", store: "Amazon", category: "Áudio", image: headphones, price: 1599, originalPrice: 2299, votes: 52 },
  { id: "7373", title: "Console PlayStation 5 Slim 1TB Edição Padrão", store: "Mercado Livre", category: "Games", image: controller, price: 3499, originalPrice: 4499, votes: 412 },
];

export function isHotDeal(votes: number) {
  return votes >= HOT_DEAL_THRESHOLD;
}
