export default function TermsOfServicePage() {
    return (
        <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-3xl mx-auto bg-white p-8 sm:p-12 shadow rounded-lg">
                <h1 className="text-3xl font-extrabold text-gray-900 mb-8">Terms of Service</h1>

                <div className="prose prose-indigo prose-lg text-gray-600">
                    <p className="leading-relaxed mb-6">Effective Date: {new Date().toLocaleDateString()}</p>

                    <h2 className="text-xl font-bold text-gray-900 mt-8 mb-4">1. Agreement to Terms</h2>
                    <p className="leading-relaxed mb-6">
                        By accessing or using the VTE (Verified Transaction Execution) platform, you agree to be bound by these Terms of Service.
                        If you disagree with any part of the terms, then you may not access the service.
                    </p>

                    <h2 className="text-xl font-bold text-gray-900 mt-8 mb-4">2. Description of Service</h2>
                    <p className="leading-relaxed mb-6">
                        VTE provides an orchestration engine and queue management system for verified transactions.
                        We reserve the right to withdraw or amend our service, and any service or material we provide via the platform, in our sole discretion without notice.
                    </p>

                    <h2 className="text-xl font-bold text-gray-900 mt-8 mb-4">3. User Accounts</h2>
                    <p className="leading-relaxed mb-6">
                        When you create an account with us, you must provide us information that is accurate, complete, and current at all times.
                        Failure to do so constitutes a breach of the Terms, which may result in immediate termination of your account on our Service.
                        You are responsible for safeguarding the password that you use to access the Service and for any activities or actions under your password.
                    </p>

                    <h2 className="text-xl font-bold text-gray-900 mt-8 mb-4">4. Intellectual Property</h2>
                    <p className="leading-relaxed mb-6">
                        The Service and its original content, features and functionality are and will remain the exclusive property of VTE and its licensors.
                        The Service is protected by copyright, trademark, and other laws of both the United States and foreign countries.
                    </p>

                    <h2 className="text-xl font-bold text-gray-900 mt-8 mb-4">5. Termination</h2>
                    <p className="leading-relaxed mb-6">
                        We may terminate or suspend your account immediately, without prior notice or liability, for any reason whatsoever, including without limitation if you breach the Terms.
                        Upon termination, your right to use the Service will immediately cease.
                    </p>

                    <h2 className="text-xl font-bold text-gray-900 mt-8 mb-4">6. Limitation of Liability</h2>
                    <p className="leading-relaxed mb-6">
                        In no event shall VTE, nor its directors, employees, partners, agents, suppliers, or affiliates, be liable for any indirect, incidental, special, consequential or punitive damages, including without limitation, loss of profits, data, use, goodwill, or other intangible losses, resulting from your access to or use of or inability to access or use the Service.
                    </p>
                </div>
            </div>
        </div>
    );
}
