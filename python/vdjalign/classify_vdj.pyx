from .codons import translate

def ref_map(list ap, int qstart=0):
    """Build a map from reference base index to query base index"""
    cdef dict result = {}
    for i, j in ap:
        if j is not None:
            result[j] = i + qstart if i is not None else None
    return result

def intersect_feature(dict rmap, feature):
    """Update a GFF feature to refer to query coordinates"""
    cdef int start0 = feature.start0, end0 = feature.end - 1
    cdef int rmin = min(rmap), rmax = max(rmap)
    cdef int any_overlap = rmin <= end0 and rmax >= start0
    cdef int complete_overlap = rmin <= start0 and rmax >= end0
    if not any_overlap:
        return None

    cdef int sstart0 = rmap[rmin if rmin > start0 else start0]
    cdef int send0 = rmap[rmax if rmax < end0 else end0]
    #print '{}: start0={} end0={} qstart0={} qend0={} rmin={} rmax={} complete={}'.format(
        #feature.attr['Name'], start0, end0, sstart0, send0, rmin, rmax, complete_overlap)

    return feature.update_attributes(complete_overlap=str(complete_overlap))\
            ._replace(start=sstart0 + 1, end=send0 + 1)

def intersect_features(dict rmap, list features):
    cdef dict r = {}
    for feature in features:
        n = feature.attribute_dict()['Name']
        r[n] = intersect_feature(rmap, feature)
    return r

def classify_record(v, d, j, dict v_annot, dict j_annot):
    vm = ref_map(v.aligned_pairs, v.qstart)
    jm = ref_map(j.aligned_pairs, j.qstart)

    # Translate features
    v_trans = intersect_features(vm, v_annot.values())
    j_trans = intersect_features(jm, j_annot.values())

    result = {}

    # CDR3 length
    cys = v_trans['Cys']
    tryp = j_trans['J-Tryp']
    if cys and cys.attr['complete_overlap'] == '1':
        result['frame'] = cys.start0 % 3
        result['amino_acid'] = translate(v.seq[cys.start0 % 3:])
    if (cys and tryp and
        cys.attr['complete_overlap'] == '1' and
        tryp.attr['complete_overlap'] == '1'):
        result['cdr3_start'] = cys.start0
        result['cdr3_end'] = tryp.end
        result['cdr3_length'] = tryp.end - cys.start0
        result['cdr3_aa'] = translate(v.seq[cys.start0:tryp.end])

    features = ((n, feat) for i in [v_trans, j_trans]
                for n, feat in i.iteritems()
                if feat is not None)

    for (gene, alignment) in [('v', v), ('d', d), ('j', j)]:
        result['{0}_nm'.format(gene)] = alignment.opt('NM')
        result['{0}_qstart'.format(gene)] = alignment.qstart
        result['{0}_qend'.format(gene)] = alignment.qend

    for n, feature in features:
        result['{0}_begin'.format(n)] = feature.start0
        result['{0}_end'.format(n)] = feature.end
        result['{0}_complete'.format(n)] = feature.attr['complete_overlap'] == '1'

    return result
