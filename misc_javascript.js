const str1 = 'silent';
const str2 = 'listen';
const str3 = 'netsil';
const str4 = 'asdfdsa';
const str5 = 'qwerttrewq';
const str6 = 'string';
const numarr = [1,2,3,4,5,6,7,8,9,8,7,6,5,4,3,22,11,6,3,6,7,2,3,4,5,5,5,5,4,5,4,3,4,3,4,2,1,1];

/* ---------------------- */
// FIBONACCI
const fibonacci = (function(){
    const memo = [0, 1];
    const _fibonacci = (n) => {
        let result = memo[n];
        if (typeof result !== "number"){
            result = _fibonacci(n - 1) + _fibonacci(n - 2);
            memo[n] = result;
        }
        return result;
    }
    return _fibonacci;
}());

/* ---------------------- */
// PALINDROME
const isPlaindrome = (str1, str2="") => {
    if (str2 === "") {
        if (str1.split("").reverse().join("") === str1) {
            console.log(`${str1} is a palindrome.`)
            return true;
        } else {
            console.log(`${str1} is not a palindrome.`)
        }
    } else {
        if (str1.split("").reverse().join("") === str2) {
            console.log(`${str1} and ${str2} are palindromes.`)
            return true;
        } else {
            console.log(`${str1} and ${str2} are not palindromes.`)
        }
    }
    return false;
}

/* ---------------------- */
// Recursive Palindrome
const recPal = (str) => {
    if (str.length <= 1) {
        return true;
    }
    
    if (str.split("")[0] === str.split("")[str.length - 1]) {
        return recPal(str.substring(1, str.length - 1));
    } else {
        return false;
    }
}

/* ---------------------- */
// REVERSE STRING
const reverseString = (str) => {
    let revStr = [];
    for (let i = 0; i < str.split("").length + 1; i++) {
        revStr[i] = str.split("")[str.split("").length - i];
    }
    return revStr.join("");
}

/* ---------------------- */
// ANAGRAM
const isAnagram = (str1, str2) => {
    if (str1.split("").sort().join("") === str2.split("").sort().join("")) {
        console.log(`${str1} and ${str2} are anagrams.`)
        return true;
    } else {
        console.log(`${str1} and ${str2} are not anagrams.`)
        return false;
    }
};

/* ---------------------- */
// WORD FREQUENCY
const freqCount = (str) => {
    const words = str.replace(/[.]/g, '').split(/\s/);
    const freqMap = {};
    words.forEach(function(word) {
        if (!freqMap[word]) {
            freqMap[word] = 0;
        }
        freqMap[word]++;
    });
    return freqMap;
}

/* ---------------------- */
// MAX VALUE IN ARRAY
const findMaxValue = (testArray) => {
    let highValue = testArray[0];
    testArray.forEach( (value) => {
        if (value > highValue){
            highValue = value;
        }
    });
    return highValue;
};

const findMaxShort = (testArray) => {
    return testArray.sort((a, b) => a - b)[testArray.length - 1];
}

/* ---------------------- */
// prime list
const isPrime = (n) => {
    for (let i = 2; i < n; i++) {
        if (n % i === 0) {
            return false;
        }
    }
    return true;
};

const listPrimes = (n) => {
    const primes = n >= 2 ? [2] : [];
    for (let i = 3; i < n; i+= 2) {
        if ( isPrime(i) ) {
            primes.push(i);
        }
    }
    return primes;
};

/* ---------------------- */
// return number in middle of list
const midPoint = (numlist) => {
    return numlist[Math.floor(numlist.length / 2)];
};

/* ---------------------- */
// unique characters
const findUnique = (str) => {
    const strArray = str.split("");
    const unique = [strArray[0]];
    for (let i = 1; i < strArray.length; i++){
        if (!unique.includes(strArray[i])) {
            unique.push(strArray[i]);
        }
    }
    return unique.join("");
};

/* ---------------------- */
// greatest common divisor
const gcd = (a, b) => {
    if (!b) {
      return a;
    }
    return gcd(b, a % b);
  }

/* ---------------------- */
// NUMBER FREQUENCY
const findMode = (arr) => {
    const numFreq = {};
    arr.forEach(function(num) {
        if (!numFreq[num]) {
            numFreq[num] = 0;
        }
        numFreq[num]++;
    });
    return Object.keys(numFreq).reduce((a, b) => numFreq[a] > numFreq[b] ? a : b);
}

// PASSWORD GENERATOR
const genPass = (passLength, numSpecialChars=0) => {
    let tempPass = Math.random().toString(36).substring(2, passLength + 2).split("").map(
        (str) => Math.round(Math.random()) ? str.toUpperCase() : str.toLowerCase()
    );
    if (numSpecialChars === 0){
        return tempPass.join("");
    } else {
        const charList = "!@#$%^&*_+."
        tempPass.splice(-numSpecialChars);
        for (let i = 0; i < numSpecialChars; i++){
            let charSeed = Math.floor(Math.random() * charList.length);
            tempPass.push(charList.substring(charSeed, charSeed + 1));
        }
        return tempPass.sort(() => {return 0.5 - Math.random()}).join("");
    }
}
