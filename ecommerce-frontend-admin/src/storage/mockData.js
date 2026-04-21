export const mockProducts = [
  {
    id: '1',
    name: 'Wireless Bluetooth Headphones',
    price: 79.99,
    image: 'https://placehold.co/400x400?text=Headphones',
    category: 'Electronics', categoryName: 'Electronics', categoryId: 1,
    stock: 25, availableQuantity: 25,
    description: 'Premium wireless headphones with active noise cancellation, 30-hour battery life, and comfortable over-ear design. Perfect for music lovers and remote workers.',
    rating: 4.5
  },
  {
    id: '2',
    name: 'Smartphone Stand & Charger',
    price: 34.99,
    image: 'https://placehold.co/400x400?text=Phone+Stand',
    category: 'Electronics', categoryName: 'Electronics', categoryId: 1,
    stock: 50, availableQuantity: 50,
    description: 'Adjustable smartphone stand with built-in 15W wireless charging. Compatible with all Qi-enabled devices. Non-slip base for stable placement.',
    rating: 4.2
  },
  {
    id: '3',
    name: 'USB-C Hub 7-in-1',
    price: 49.99,
    image: 'https://placehold.co/400x400?text=USB+Hub',
    category: 'Electronics', categoryName: 'Electronics', categoryId: 1,
    stock: 30, availableQuantity: 30,
    description: 'Expand your laptop connectivity with HDMI 4K, 3x USB 3.0, SD card reader, and 100W PD charging port. Plug and play, no drivers required.',
    rating: 4.7
  },
  {
    id: '4',
    name: 'Mechanical Keyboard',
    price: 129.99,
    image: 'https://placehold.co/400x400?text=Keyboard',
    category: 'Electronics', categoryName: 'Electronics', categoryId: 1,
    stock: 15, availableQuantity: 15,
    description: 'Compact TKL mechanical keyboard with Cherry MX Red switches. RGB backlit keys, aluminum frame, and detachable USB-C cable.',
    rating: 4.8
  },
  {
    id: '5',
    name: 'Classic Cotton T-Shirt',
    price: 19.99,
    image: 'https://placehold.co/400x400?text=T-Shirt',
    category: 'Clothing', categoryName: 'Clothing', categoryId: 2,
    stock: 100, availableQuantity: 100,
    description: '100% organic cotton crew-neck t-shirt. Pre-shrunk, breathable fabric available in a range of sizes. Machine washable.',
    rating: 4.3
  },
  {
    id: '6',
    name: 'Slim Fit Chino Pants',
    price: 44.99,
    image: 'https://placehold.co/400x400?text=Chinos',
    category: 'Clothing', categoryName: 'Clothing', categoryId: 2,
    stock: 60, availableQuantity: 60,
    description: 'Versatile slim-fit chino pants made from stretch cotton blend. Suitable for casual and semi-formal occasions. Available in multiple colors.',
    rating: 4.1
  },
  {
    id: '7',
    name: 'Hooded Zip-Up Sweatshirt',
    price: 54.99,
    image: 'https://placehold.co/400x400?text=Hoodie',
    category: 'Clothing', categoryName: 'Clothing', categoryId: 2,
    stock: 45, availableQuantity: 45,
    description: 'Cozy fleece-lined hoodie with kangaroo pocket and adjustable drawstring. Perfect for layering on cool days.',
    rating: 4.6
  },
  {
    id: '8',
    name: 'JavaScript: The Good Parts',
    price: 24.99,
    image: 'https://placehold.co/400x400?text=JS+Book',
    category: 'Books', categoryName: 'Books', categoryId: 3,
    stock: 20, availableQuantity: 20,
    description: 'A classic guide to JavaScript best practices by Douglas Crockford. Essential reading for any web developer looking to master the language.',
    rating: 4.9
  },
  {
    id: '9',
    name: 'Clean Code',
    price: 29.99,
    image: 'https://placehold.co/400x400?text=Clean+Code',
    category: 'Books', categoryName: 'Books', categoryId: 3,
    stock: 18, availableQuantity: 18,
    description: "Robert C. Martin's handbook of agile software craftsmanship. Learn how to write readable, maintainable, and robust code.",
    rating: 4.8
  },
  {
    id: '10',
    name: 'The Pragmatic Programmer',
    price: 32.99,
    image: 'https://placehold.co/400x400?text=Pragmatic',
    category: 'Books', categoryName: 'Books', categoryId: 3,
    stock: 22, availableQuantity: 22,
    description: 'A timeless guide to software development best practices. Covers topics from career development to technical excellence.',
    rating: 4.7
  },
  {
    id: '11',
    name: 'Ceramic Coffee Mug Set',
    price: 27.99,
    image: 'https://placehold.co/400x400?text=Mug+Set',
    category: 'Home', categoryName: 'Home', categoryId: 4,
    stock: 35, availableQuantity: 35,
    description: 'Set of 4 handcrafted ceramic mugs, 12oz each. Microwave and dishwasher safe. Minimalist design complements any kitchen style.',
    rating: 4.4
  },
  {
    id: '12',
    name: 'Bamboo Desk Organizer',
    price: 39.99,
    image: 'https://placehold.co/400x400?text=Organizer',
    category: 'Home', categoryName: 'Home', categoryId: 4,
    stock: 28, availableQuantity: 28,
    description: 'Eco-friendly bamboo desk organizer with 5 compartments for pens, papers, and accessories. Keeps your workspace tidy and stylish.',
    rating: 4.5
  }
];

export const mockUsers = [
  {
    id: 'u1',
    email: 'john@example.com',
    password: 'password123',
    firstName: 'John',
    lastName: 'Doe',
    registeredDate: '2025-04-12',
    address: { street: 'Main St', houseNumber: '123', zipCode: '62701' }
  },
  {
    id: 'u2',
    email: 'jane@example.com',
    password: 'password456',
    firstName: 'Jane',
    lastName: 'Smith',
    registeredDate: '2025-06-08',
    address: { street: 'Oak Ave', houseNumber: '456', zipCode: '97201' }
  },
  {
    id: 'u3',
    email: 'mike.johnson@example.com',
    password: 'password789',
    firstName: 'Mike',
    lastName: 'Johnson',
    registeredDate: '2025-08-20',
    address: { street: 'Elm St', houseNumber: '789', zipCode: '10001' }
  },
  {
    id: 'u4',
    email: 'sarah.w@example.com',
    password: 'passwordabc',
    firstName: 'Sarah',
    lastName: 'Williams',
    registeredDate: '2025-09-05',
    address: { street: 'Pine Rd', houseNumber: '22', zipCode: '30301' }
  },
  {
    id: 'u5',
    email: 'david.brown@example.com',
    password: 'passworddef',
    firstName: 'David',
    lastName: 'Brown',
    registeredDate: '2025-10-14',
    address: { street: 'Maple Dr', houseNumber: '55', zipCode: '60601' }
  },
  {
    id: 'u6',
    email: 'emily.davis@example.com',
    password: 'passwordghi',
    firstName: 'Emily',
    lastName: 'Davis',
    registeredDate: '2025-11-30',
    address: { street: 'Cedar Ln', houseNumber: '8', zipCode: '77001' }
  },
  {
    id: 'u7',
    email: 'chris.wilson@example.com',
    password: 'passwordjkl',
    firstName: 'Chris',
    lastName: 'Wilson',
    registeredDate: '2026-01-18',
    address: { street: 'Birch Blvd', houseNumber: '301', zipCode: '85001' }
  }
];

export const mockOrders = [
  {
    id: 'a1b2c3d4-e5f6-7890-abcd-ef1234567801',
    userUid: 'u1',
    status: 'PAID',
    totalAmount: 129.97,
    createdAt: '2025-10-15T10:30:00Z',
    items: [
      { uid: 'i01a', productUid: '1', quantity: 1, priceSnapshot: 79.99 },
      { uid: 'i01b', productUid: '8', quantity: 2, priceSnapshot: 24.99 },
    ],
  },
  {
    id: 'a1b2c3d4-e5f6-7890-abcd-ef1234567802',
    userUid: 'u1',
    status: 'PAID',
    totalAmount: 129.99,
    createdAt: '2025-11-20T14:15:00Z',
    items: [
      { uid: 'i02a', productUid: '4', quantity: 1, priceSnapshot: 129.99 },
    ],
  },
  {
    id: 'a1b2c3d4-e5f6-7890-abcd-ef1234567803',
    userUid: 'u2',
    status: 'PAID',
    totalAmount: 87.96,
    createdAt: '2025-11-28T09:00:00Z',
    items: [
      { uid: 'i03a', productUid: '5', quantity: 3, priceSnapshot: 19.99 },
      { uid: 'i03b', productUid: '11', quantity: 1, priceSnapshot: 27.99 },
    ],
  },
  {
    id: 'a1b2c3d4-e5f6-7890-abcd-ef1234567804',
    userUid: 'u3',
    status: 'PAID',
    totalAmount: 79.98,
    createdAt: '2025-12-05T16:45:00Z',
    items: [
      { uid: 'i04a', productUid: '3', quantity: 1, priceSnapshot: 49.99 },
      { uid: 'i04b', productUid: '9', quantity: 1, priceSnapshot: 29.99 },
    ],
  },
  {
    id: 'a1b2c3d4-e5f6-7890-abcd-ef1234567805',
    userUid: 'u4',
    status: 'PAID',
    totalAmount: 149.97,
    createdAt: '2025-12-18T11:20:00Z',
    items: [
      { uid: 'i05a', productUid: '7', quantity: 2, priceSnapshot: 54.99 },
      { uid: 'i05b', productUid: '12', quantity: 1, priceSnapshot: 39.99 },
    ],
  },
  {
    id: 'a1b2c3d4-e5f6-7890-abcd-ef1234567806',
    userUid: 'u2',
    status: 'PAID',
    totalAmount: 209.98,
    createdAt: '2026-01-08T08:30:00Z',
    items: [
      { uid: 'i06a', productUid: '1', quantity: 1, priceSnapshot: 79.99 },
      { uid: 'i06b', productUid: '4', quantity: 1, priceSnapshot: 129.99 },
    ],
  },
  {
    id: 'a1b2c3d4-e5f6-7890-abcd-ef1234567807',
    userUid: 'u5',
    status: 'PAID',
    totalAmount: 57.98,
    createdAt: '2026-01-15T13:00:00Z',
    items: [
      { uid: 'i07a', productUid: '10', quantity: 1, priceSnapshot: 32.99 },
      { uid: 'i07b', productUid: '8', quantity: 1, priceSnapshot: 24.99 },
    ],
  },
  {
    id: 'a1b2c3d4-e5f6-7890-abcd-ef1234567808',
    userUid: 'u6',
    status: 'PAID',
    totalAmount: 124.97,
    createdAt: '2026-01-22T17:10:00Z',
    items: [
      { uid: 'i08a', productUid: '2', quantity: 1, priceSnapshot: 34.99 },
      { uid: 'i08b', productUid: '6', quantity: 2, priceSnapshot: 44.99 },
    ],
  },
  {
    id: 'a1b2c3d4-e5f6-7890-abcd-ef1234567809',
    userUid: 'u3',
    status: 'PAID',
    totalAmount: 95.97,
    createdAt: '2026-02-10T10:05:00Z',
    items: [
      { uid: 'i09a', productUid: '11', quantity: 2, priceSnapshot: 27.99 },
      { uid: 'i09b', productUid: '12', quantity: 1, priceSnapshot: 39.99 },
    ],
  },
  {
    id: 'a1b2c3d4-e5f6-7890-abcd-ef1234567810',
    userUid: 'u7',
    status: 'PAID',
    totalAmount: 179.98,
    createdAt: '2026-02-14T12:30:00Z',
    items: [
      { uid: 'i10a', productUid: '4', quantity: 1, priceSnapshot: 129.99 },
      { uid: 'i10b', productUid: '3', quantity: 1, priceSnapshot: 49.99 },
    ],
  },
  {
    id: 'a1b2c3d4-e5f6-7890-abcd-ef1234567811',
    userUid: 'u1',
    status: 'PAID',
    totalAmount: 94.97,
    createdAt: '2026-02-20T15:45:00Z',
    items: [
      { uid: 'i11a', productUid: '5', quantity: 2, priceSnapshot: 19.99 },
      { uid: 'i11b', productUid: '7', quantity: 1, priceSnapshot: 54.99 },
    ],
  },
  {
    id: 'a1b2c3d4-e5f6-7890-abcd-ef1234567812',
    userUid: 'u4',
    status: 'PAID',
    totalAmount: 62.98,
    createdAt: '2026-03-05T09:20:00Z',
    items: [
      { uid: 'i12a', productUid: '9', quantity: 1, priceSnapshot: 29.99 },
      { uid: 'i12b', productUid: '10', quantity: 1, priceSnapshot: 32.99 },
    ],
  },
  {
    id: 'a1b2c3d4-e5f6-7890-abcd-ef1234567813',
    userUid: 'u5',
    status: 'PENDING',
    totalAmount: 79.99,
    createdAt: '2026-03-12T11:00:00Z',
    items: [
      { uid: 'i13a', productUid: '1', quantity: 1, priceSnapshot: 79.99 },
    ],
  },
  {
    id: 'a1b2c3d4-e5f6-7890-abcd-ef1234567814',
    userUid: 'u6',
    status: 'PENDING',
    totalAmount: 107.97,
    createdAt: '2026-03-18T14:30:00Z',
    items: [
      { uid: 'i14a', productUid: '12', quantity: 2, priceSnapshot: 39.99 },
      { uid: 'i14b', productUid: '11', quantity: 1, priceSnapshot: 27.99 },
    ],
  },
  {
    id: 'a1b2c3d4-e5f6-7890-abcd-ef1234567815',
    userUid: 'u2',
    status: 'PENDING',
    totalAmount: 104.96,
    createdAt: '2026-03-22T08:45:00Z',
    items: [
      { uid: 'i15a', productUid: '6', quantity: 1, priceSnapshot: 44.99 },
      { uid: 'i15b', productUid: '5', quantity: 3, priceSnapshot: 19.99 },
    ],
  },
  {
    id: 'a1b2c3d4-e5f6-7890-abcd-ef1234567816',
    userUid: 'u7',
    status: 'CANCELLED',
    totalAmount: 54.99,
    createdAt: '2026-04-01T10:00:00Z',
    items: [
      { uid: 'i16a', productUid: '7', quantity: 1, priceSnapshot: 54.99 },
    ],
  },
  {
    id: 'a1b2c3d4-e5f6-7890-abcd-ef1234567817',
    userUid: 'u3',
    status: 'CANCELLED',
    totalAmount: 49.99,
    createdAt: '2026-04-10T16:00:00Z',
    items: [
      { uid: 'i17a', productUid: '3', quantity: 1, priceSnapshot: 49.99 },
    ],
  },
];

export const mockAdminUsers = [
  {
    id: 'a1',
    email: 'admin@shopapp.com',
    password: 'admin123',
    firstName: 'Admin',
    lastName: 'User',
    role: 'admin'
  }
];

// Monthly analytics data (last 12 months: Apr 2025 – Mar 2026)
export const monthlyStats = [
  { month: 'Apr', revenue: 1240, orders: 9 },
  { month: 'May', revenue: 1870, orders: 13 },
  { month: 'Jun', revenue: 2150, orders: 16 },
  { month: 'Jul', revenue: 1920, orders: 14 },
  { month: 'Aug', revenue: 2580, orders: 19 },
  { month: 'Sep', revenue: 3100, orders: 23 },
  { month: 'Oct', revenue: 3450, orders: 26 },
  { month: 'Nov', revenue: 4200, orders: 33 },
  { month: 'Dec', revenue: 5850, orders: 46 },
  { month: 'Jan', revenue: 3920, orders: 30 },
  { month: 'Feb', revenue: 4380, orders: 34 },
  { month: 'Mar', revenue: 2920, orders: 22 },
];
