from flask import Flask, request, render_template
import joblib
import numpy as np

app = Flask(__name__)

model  = joblib.load('Prediction Model')

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/predict', methods=['GET', 'POST'])


def predict():
    if request.method ==  'POST':
        gender = request.form['gender']
        married = request.form['married']
        dependents = request.form['dependents']
        education = request.form['education']
        employed = request.form['employed']
        credit = float(request.form['credit'])
        area = request.form['area']
        ApplicantIncome = request.form['ApplicantIncome'] 
        ApplicantIncome = ApplicantIncome.replace(",", "") 
        ApplicantIncome = float(ApplicantIncome)
        CoapplicantIncome = request.form['CoapplicantIncome'] 
        CoapplicantIncome = CoapplicantIncome.replace(",", "") 
        CoapplicantIncome = float(CoapplicantIncome)
        LoanAmount = request.form['LoanAmount'] 
        LoanAmount = LoanAmount.replace(",", "") 
        LoanAmount = float(LoanAmount)
        Loan_Amount_Term = request.form['Loan_Amount_Term'] 
        if "year" in Loan_Amount_Term.lower():
             Loan_Amount_Term = Loan_Amount_Term.lower() 
             Loan_Amount_Term = Loan_Amount_Term.replace("years", "")
             Loan_Amount_Term = Loan_Amount_Term.replace("year", "")
             Loan_Amount_Term = Loan_Amount_Term.strip()
             Loan_Amount_Term = float(Loan_Amount_Term) * 12 
        else:
             Loan_Amount_Term = float(Loan_Amount_Term)

        # gender
        if (gender == "Male"):
            male=1
        else:
            male=0
        
        # married
        if(married=="Yes"):
            married_yes = 1
        else:
            married_yes=0

        # dependents
        if(dependents=='1'):
            dependents_1 = 1
            dependents_2 = 0
            dependents_3 = 0
        elif(dependents == '2'):
            dependents_1 = 0
            dependents_2 = 1
            dependents_3 = 0
        elif(dependents=="3+"):
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 1
        else:
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 0  

        # education
        if (education=="Not Graduate"):
            not_graduate=1
        else:
            not_graduate=0

        # employed
        if (employed == "Yes"):
            employed_yes=1
        else:
            employed_yes=0

        # property area

        if(area=="Semiurban"):
            semiurban=1
            urban=0
        elif(area=="Urban"):
            semiurban=0
            urban=1
        else:
            semiurban=0
            urban=0


        ApplicantIncomelog = np.log(ApplicantIncome)
        totalincomelog = np.log(ApplicantIncome+CoapplicantIncome)
        LoanAmountlog = np.log(LoanAmount)
        Loan_Amount_Termlog = np.log(Loan_Amount_Term)

        prediction = model.predict([[credit, ApplicantIncomelog,LoanAmountlog, Loan_Amount_Termlog, totalincomelog, male, married_yes, dependents_1, dependents_2, dependents_3, not_graduate, employed_yes,semiurban, urban ]])

        # print(prediction)

        if(prediction=="N"):
            prediction="Sorry , You are not Eligible to avail loan services"
        else:
            prediction="Congratualtions , You Can avail loan services"


        return render_template("prediction.html", prediction_text="{}".format(prediction))

    else:
        return render_template("prediction.html")



        
if __name__ == "__main__":
    app.run(debug=True , host='0.0.0.0')
