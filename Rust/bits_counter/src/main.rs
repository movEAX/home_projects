static MASKS: [u64; 6] = [
    0x5555555555555555,
    0x3333333333333333,
    0x0f0f0f0f0f0f0f0f,
    0x00ff00ff00ff00ff,
    0x0000ffff0000ffff,
    0x00000000ffffffff
];

fn bits_count(mut val:u64) -> u8 {
    for i in 0..6 {
        let shift = 1 << i;
        let mask = MASKS[i];
        val = (val & mask) + ((val >> shift) & mask)
    }

    val as u8   
}

fn main() {
    println!("Bits count: {}", bits_count(7));
}
