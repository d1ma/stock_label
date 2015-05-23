import os
import sys

base_dir = None
out_dir = None

def process_company(company_name):
    company_str = ""
    company_path = os.path.join(base_dir, company_name)
    available_dirs = os.listdir(company_path)
    cert_dirs = filter(lambda x: x.find("ertificate") >= 0, available_dirs)
    if len(cert_dirs) == 0:
        sys.stderr.write("Could not process %s. " % company_name)
        sys.stderr.write("Available dirs: %s" % ", ".join(available_dirs))
        return ""
    elif len(cert_dirs) > 1:
        sys.stderr.write("More than one cert folder in %s " % company_name)
        return ""

    try:
        ####### [ Take the first dir containing name certificate ] ###
        cert_path =  os.path.join(company_path, cert_dirs[0])
        files = os.listdir(cert_path)
    except OSError:
        return ""
    for f in files:
        cert = os.path.join(cert_path, f)
        out_cert = os.path.join(out_dir, f)
        with open(cert) as input_file:
            with open(out_cert, 'w') as output_file:
                contents = input_file.read()
                company_str += contents + "\n\n"
                output_file.write(contents)
    return company_str

def main():
    global base_dir, out_dir

    base_dir = sys.argv[1]
    out_dir = sys.argv[2]

    companies = os.listdir(base_dir)
    for comp in companies:
        process_company(comp)


if __name__=="__main__":
    if len(sys.argv) != 3:
        print "Usage: python make_dump.py base_dir/ out_dir/"
    else:
        main()
