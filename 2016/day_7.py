from util.decorators import aoc_output_formatter
from util.input import get_input

#---------------------------------------------------------------------------------------------------

def _contains_abba(val):
    """ Returns if a string sequence contains an ABBA, which is a 4 character sequence where a
    pair of different characters is followed by its reverse. Ex: abba, xyyz, haah, ette """

    for i in range(0, len(val)-3):
        substr = val[i:i+4]
        if substr == ''.join(reversed(substr)):
            if substr[0] == substr[1]:
                continue
            return True
    return False


def _get_all_aba(val):
    """ Returns all ABA sequences present in a string, which is a 3 character sequence of the form
    ABA where the inner letter B differs from the framing As. """

    aba_sequences = list()
    for i in range(0, len(val)-2):
        substr = val[i:i+3]
        if substr == ''.join(reversed(substr)):
            if substr[0] == substr[1]:
                continue
            aba_sequences.append(substr)
    return aba_sequences


def _extract_hypernet_sequences(ip):
    """ Extracts the hypernet sequences from the IP and returns a list of them.
    Ex: "abc[def]gh[ijk]lm" -> ["def", "ijk"] """

    # Find all bracket pairs and extract them and their contents from the IPv7 address
    raw_bracket_indexes = [i for i, char in enumerate(ip) if char in '[]']

    hypernet_sequences = list()
    while raw_bracket_indexes:
        start_ix = raw_bracket_indexes.pop(0)
        end_ix = raw_bracket_indexes.pop(0)
        hypernet_sequences.append(ip[start_ix+1:end_ix])

    return hypernet_sequences


def _remove_hypernet_sequences(hypernet_sequences, ip):
    """ Removes hypernet_sequences from the IP and returns the remaining pieces in a list.
    Ex: "abc[def]gh[ijk]lm" --> ["abc", "gh", "lm"] """

    # Remove the portions of the IP which are hypernet sequences
    for sequence in hypernet_sequences:
        ip = ip.replace(sequence, '')

    # Remove the bracket pairs, leaving spaces so we can split the string on those spaces and
    # return the remaining IP pieces as a list.
    return ip.replace('[]', ' ').split(' ')


def _does_ip_support_tls(ip):
    """ Returns whether the IPv7 address supports TLS. If the any hypernet sequences (within square
    brackets) contain an ABBA (character pair followed by its reverse), then address does not
    support TLS. If an ABBA is present anywhere else, it does support TLS. """

    hypernet_sequences = _extract_hypernet_sequences(ip)

    # If any of the hypernet sequences contain an ABBA, the IP does not support TLS
    if any([_contains_abba(sequence) for sequence in hypernet_sequences]):
        return False

    ip_chunks = _remove_hypernet_sequences(hypernet_sequences, ip)

    # If any of the remaining portions of the IP have an ABBA, it supports TLS.
    return any(_contains_abba(ip_chunk) for ip_chunk in ip_chunks)


def _does_ip_support_ssl(ip):
    """ Returns whether the IPv7 address supports SLS, which requires an ABA sequence to exist
    outside of the hypernet sequences and a corresponding BAB sequence to be within one of the
    hypernet sequences. """

    bab = lambda val: val[1:] + val[1]

    # Extract out the hypernet sequences and the remaining chunks of IP
    hypernet_sequences = _extract_hypernet_sequences(ip)
    ip_chunks = _remove_hypernet_sequences(hypernet_sequences, ip)

    # Get all ABA in the IP chunks
    aba_sequences = list()
    for ip_chunk in ip_chunks:
        aba_sequences.extend(_get_all_aba(ip_chunk))

    # Get all ABA in the hypernet sequences, calling them a BAB
    bab_sequences = list()
    for hypernet_seq in hypernet_sequences:
        bab_sequences.extend(_get_all_aba(hypernet_seq))

    # Check if the BAB version of any ABA from IP chunks, exist in the BAB for hypernet sequences
    return any(bab(aba) in bab_sequences for aba in aba_sequences)

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2016, 7, 1, 'number of IPs supporting TLS')
def part_one(ips):
    return sum([1 for ip in ips if _does_ip_support_tls(ip)])


@aoc_output_formatter(2016, 7, 2, 'number of IPs supporting SSL')
def part_two(ips):
    return sum([1 for ip in ips if _does_ip_support_ssl(ip)])

#---------------------------------------------------------------------------------------------------

def run(input_file):

    ips = get_input(input_file)

    part_one(ips)
    part_two(ips)
