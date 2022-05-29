# No Imports Allowed!


def backwards(sound):
    '''Return a reversed sound. It does not modify input'''
    return {
        'rate': sound['rate'],
        'samples': sound['samples'][::-1],
    }


def mix(sound1, sound2, p):
    '''Mix two sounds together and return new sound
    
    The resulting sound should take p times the samples in the first sound
    and 1-p times the samples in the second sound, and add them together to
    produce a new sound.
    The two input sounds should have the same sampling rate. Return None otherwise.
    If sounds have different durations, then length of resulting sound should be
    minimum of the length of the input sounds.
    '''
    if sound1['rate'] == sound2['rate']:
        new_sound = [first_sample * p + second_sample * (1 - p)
            for first_sample, second_sample in zip(sound1['samples'], sound2['samples'])]
        return {
            'rate': sound1['rate'],
            'samples': new_sound,
        }


def convolve(sound, kernel):
    '''Apply convolution operator to the samples in a sound and a kernel'''
    convolved_samples = [0.] * (len(sound['samples']) + len(kernel) - 1)
    for shift, scale in enumerate(kernel):
        samples = [0.] * shift + [sample * scale for sample in sound['samples']] + [0.] * (len(kernel) - shift - 1)
        convolved_samples = [sum(values) for values in zip(samples, convolved_samples)]
    return {
        'rate': sound['rate'],
        'samples': convolved_samples,
    }


def echo(sound, num_echoes, delay, scale):
    '''Apply echo filter'''
    sample_delay = round(delay * sound['rate'])
    resulting_samples = [0.] * (len(sound['samples']) + sample_delay * num_echoes)
    for i in range(num_echoes + 1):
        iteration_scale = scale ** i
        part_of_samples = [sample * iteration_scale for sample in sound['samples']]
        samples = [0.] * i * sample_delay + part_of_samples + [0.] * (num_echoes - i) * sample_delay
        resulting_samples = [sum(values) for values in zip(samples, resulting_samples)]
    return {
        'rate': sound['rate'],
        'samples': resulting_samples,
    }


def pan(sound):
    raise NotImplementedError


def remove_vocals(sound):
    raise NotImplementedError


def bass_boost_kernel(N, scale=0):
    """
    Construct a kernel that acts as a bass-boost filter.

    We start by making a low-pass filter, whose frequency response is given by
    (1/2 + 1/2cos(Omega)) ^ N

    Then we scale that piece up and add a copy of the original signal back in.
    """
    # make this a fake "sound" so that we can use the convolve function
    base = {'rate': 0, 'samples': [0.25, 0.5, 0.25]}
    kernel = {'rate': 0, 'samples': [0.25, 0.5, 0.25]}
    for i in range(N):
        kernel = convolve(kernel, base['samples'])
    kernel = kernel['samples']

    # at this point, the kernel will be acting as a low-pass filter, so we
    # scale up the values by the given scale, and add in a value in the middle
    # to get a (delayed) copy of the original
    kernel = [i * scale for i in kernel]
    kernel[len(kernel)//2] += 1

    return kernel


# below are helper functions for converting back-and-forth between WAV files
# and our internal dictionary representation for sounds

import io
import wave
import struct

def load_wav(filename, stereo=False):
    """
    Given the filename of a WAV file, load the data from that file and return a
    Python dictionary representing that sound
    """
    f = wave.open(filename, 'r')
    chan, bd, sr, count, _, _ = f.getparams()

    assert bd == 2, "only 16-bit WAV files are supported"

    out = {'rate': sr}

    if stereo:
        left = []
        right = []
        for i in range(count):
            frame = f.readframes(1)
            if chan == 2:
                left.append(struct.unpack('<h', frame[:2])[0])
                right.append(struct.unpack('<h', frame[2:])[0])
            else:
                datum = struct.unpack('<h', frame)[0]
                left.append(datum)
                right.append(datum)

        out['left'] = [i/(2**15) for i in left]
        out['right'] = [i/(2**15) for i in right]
    else:
        samples = []
        for i in range(count):
            frame = f.readframes(1)
            if chan == 2:
                left = struct.unpack('<h', frame[:2])[0]
                right = struct.unpack('<h', frame[2:])[0]
                samples.append((left + right)/2)
            else:
                datum = struct.unpack('<h', frame)[0]
                samples.append(datum)

        out['samples'] = [i/(2**15) for i in samples]

    return out


def write_wav(sound, filename):
    """
    Given a dictionary representing a sound, and a filename, convert the given
    sound into WAV format and save it as a file with the given filename (which
    can then be opened by most audio players)
    """
    outfile = wave.open(filename, 'w')

    if 'samples' in sound:
        # mono file
        outfile.setparams((1, 2, sound['rate'], 0, 'NONE', 'not compressed'))
        out = [int(max(-1, min(1, v)) * (2**15-1)) for v in sound['samples']]
    else:
        # stereo
        outfile.setparams((2, 2, sound['rate'], 0, 'NONE', 'not compressed'))
        out = []
        for l, r in zip(sound['left'], sound['right']):
            l = int(max(-1, min(1, l)) * (2**15-1))
            r = int(max(-1, min(1, r)) * (2**15-1))
            out.append(l)
            out.append(r)

    outfile.writeframes(b''.join(struct.pack('<h', frame) for frame in out))
    outfile.close()


if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place to put your
    # code for generating and saving sounds, or any other code you write for
    # testing, etc.

    # here is an example of loading a file (note that this is specified as
    # sounds/hello.wav, rather than just as hello.wav, to account for the
    # sound files being in a different directory than this file)
    mystery = load_wav('sounds/mystery.wav')
    write_wav(backwards(mystery), 'answers/mystery_reversed.wav')

    synth = load_wav('sounds/synth.wav')
    water = load_wav('sounds/water.wav')
    write_wav(mix(synth, water, p=0.2), 'answers/mix_sound.wav')

    ice_and_chilli = load_wav('sounds/ice_and_chilli.wav')
    bass_kernel = bass_boost_kernel(N=1000, scale= 1.5)
    write_wav(convolve(ice_and_chilli, bass_kernel), 'answers/bass_ice_and_chilli.wav')

    chord = load_wav('sounds/chord.wav')
    write_wav(echo(chord, 5, 0.3, 0.6), 'answers/echo_chord.wav')
