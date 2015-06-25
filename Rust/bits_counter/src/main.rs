static MASKS: [u64; 6] = [
    0x5555555555555555,
    0x3333333333333333,
    0x0f0f0f0f0f0f0f0f,
    0x00ff00ff00ff00ff,
    0x0000ffff0000ffff,
    0x00000000ffffffff
];

fn bits_count1(mut val:u64) -> u8 {
    for i in 0..6 {
        let shift = 1 << i;
        let mask = MASKS[i];
        val = (val & mask) + ((val >> shift) & mask)
    }

    val as u8 
}

fn bits_count2(mut val:u64) -> u8 {
    let mut acc:u8 = 0;
    while val != 0 {
        acc += 1;
        val = val & (val - 1);
    }

    acc
}

fn main() {
    let num = 45635645_u64;
    assert_eq!(bits_count1(num), bits_count2(num));
}
