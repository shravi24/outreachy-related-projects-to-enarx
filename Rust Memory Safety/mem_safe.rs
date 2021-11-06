#![feature(allocator_api)]

use std::heap::{Heap, Layout, Alloc};
use std::slice;

struct Vec2 {
    data: Box<[isize]>,
    length: usize,
    capacity: usize,
}

impl Vec2 {
    fn new() -> Vec2 {
        let v = Vec2 {
            data: Box::new([0]),
            length: 0,
            capacity: 1,
        };
        return v;
    }

    fn push(&mut self, n: isize) {
        if self.length == self.capacity {
            let new_capacity = self.capacity * 2;
            let mut new_data = unsafe {
                let ptr = Heap::default()
                    .alloc(Layout::array::<isize>(new_capacity).unwrap())
                    .unwrap() as *mut isize;
                Box::from_raw(slice::from_raw_parts_mut(ptr, new_capacity))
            };

            for i in 0..self.length {
                new_data[i] = self.data[i];
            }

            self.data = new_data;
            self.capacity = new_capacity;
        }

        self.data[self.length] = n;
        self.length += 1;
    }
}

fn main() {
    let mut vec: Vec2 = Vec2::new();
    vec.push(107);
    vec.push(110);

    let n: &isize = &vec.data[0];
}