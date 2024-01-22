export default function Legend() {
    return (
            <div className="absolute top-0 right-0 p-4">
                <h5>Course Fields</h5>
                <div className="flex flex-col space-y-1">
                <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 bg-red-500 rounded-full" />
                    <span className="text-sm">Red Label</span>
                </div>
                <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 bg-green-500 rounded-full" />
                    <span className="text-sm">Green Label</span>
                </div>
                <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 bg-blue-500 rounded-full" />
                    <span className="text-sm">Blue Label</span>
                </div>
                </div>
            </div>
    )
}